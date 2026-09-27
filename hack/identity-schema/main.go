package main

import (
	"encoding/base64"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"reflect"
	"sort"

	"github.com/steeltanuki/kubefacet/api/v1alpha1"
	"k8s.io/apimachinery/pkg/runtime"
	yaml "sigs.k8s.io/yaml"
)

type baseline struct {
	Resources map[string]struct {
		SourcePath string `json:"source_path"`
		SHA256     string `json:"sha256"`
		ContentB64 string `json:"content_b64"`
	} `json:"resources"`
}

type identity struct {
	file     string
	crdName  string
	kind     string
	listKind string
	plural   string
	singular string
}

var identities = map[string]identity{
	"facet": {
		file: "kubefacet.steeltanuki.it_facets.yaml", crdName: "facets.kubefacet.steeltanuki.it",
		kind: "Facet", listKind: "FacetList", plural: "facets", singular: "facet",
	},
	"access-policy": {
		file: "kubefacet.steeltanuki.it_facetaccesspolicies.yaml", crdName: "facetaccesspolicies.kubefacet.steeltanuki.it",
		kind: "FacetAccessPolicy", listKind: "FacetAccessPolicyList", plural: "facetaccesspolicies", singular: "facetaccesspolicy",
	},
}

func main() {
	if err := verify(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Println("PROJECT_IDENTITY=api STATUS=passed RESOURCES=2 SCHEMA=semantic-equivalence")
}

func verify() error {
	baselineBytes, err := os.ReadFile(".walden/specs/project-identity-rename/api-schema-baseline.json")
	if err != nil {
		return fmt.Errorf("read schema baseline: %w", err)
	}
	var archived baseline
	if err := json.Unmarshal(baselineBytes, &archived); err != nil {
		return fmt.Errorf("decode schema baseline: %w", err)
	}
	if len(archived.Resources) != len(identities) {
		return fmt.Errorf("schema baseline contains %d resources, want %d", len(archived.Resources), len(identities))
	}

	entries, err := os.ReadDir("config/crd/bases")
	if err != nil {
		return fmt.Errorf("list generated CRDs: %w", err)
	}
	var crdFiles []string
	for _, entry := range entries {
		if !entry.IsDir() && filepath.Ext(entry.Name()) == ".yaml" {
			crdFiles = append(crdFiles, entry.Name())
		}
	}
	sort.Strings(crdFiles)
	wantFiles := []string{identities["access-policy"].file, identities["facet"].file}
	sort.Strings(wantFiles)
	if !reflect.DeepEqual(crdFiles, wantFiles) {
		return fmt.Errorf("generated CRD files = %v, want exactly %v", crdFiles, wantFiles)
	}

	for key, want := range identities {
		entry, ok := archived.Resources[key]
		if !ok {
			return fmt.Errorf("schema baseline is missing %s", key)
		}
		oldBytes, err := base64.StdEncoding.DecodeString(entry.ContentB64)
		if err != nil {
			return fmt.Errorf("decode archived %s CRD: %w", key, err)
		}
		newBytes, err := os.ReadFile(filepath.Join("config/crd/bases", want.file))
		if err != nil {
			return fmt.Errorf("read generated %s CRD: %w", key, err)
		}
		var oldCRD, newCRD map[string]any
		if err := yaml.Unmarshal(oldBytes, &oldCRD); err != nil {
			return fmt.Errorf("parse archived %s CRD: %w", key, err)
		}
		if err := yaml.Unmarshal(newBytes, &newCRD); err != nil {
			return fmt.Errorf("parse generated %s CRD: %w", key, err)
		}
		if err := requireIdentity(newCRD, want); err != nil {
			return fmt.Errorf("generated %s CRD identity: %w", key, err)
		}
		if err := normalizeIdentity(oldCRD, want); err != nil {
			return fmt.Errorf("archived %s CRD shape: %w", key, err)
		}
		if err := normalizeIdentity(newCRD, want); err != nil {
			return fmt.Errorf("generated %s CRD shape: %w", key, err)
		}
		if !reflect.DeepEqual(oldCRD, newCRD) {
			oldJSON, _ := json.MarshalIndent(oldCRD, "", "  ")
			newJSON, _ := json.MarshalIndent(newCRD, "", "  ")
			return fmt.Errorf("%s generated schema differs from the archived semantic baseline\nnormalized baseline:\n%s\nnormalized generated:\n%s", key, oldJSON, newJSON)
		}
	}
	return verifyScheme()
}

func requireIdentity(crd map[string]any, want identity) error {
	metadata, ok := crd["metadata"].(map[string]any)
	if !ok || metadata["name"] != want.crdName {
		return fmt.Errorf("metadata.name = %v, want %q", valueAt(metadata, "name"), want.crdName)
	}
	spec, ok := crd["spec"].(map[string]any)
	if !ok || spec["group"] != "kubefacet.steeltanuki.it" {
		return fmt.Errorf("spec.group = %v, want %q", valueAt(spec, "group"), "kubefacet.steeltanuki.it")
	}
	names, ok := spec["names"].(map[string]any)
	if !ok {
		return fmt.Errorf("spec.names is missing")
	}
	for field, expected := range map[string]string{
		"kind": want.kind, "listKind": want.listKind, "plural": want.plural, "singular": want.singular,
	} {
		if names[field] != expected {
			return fmt.Errorf("spec.names.%s = %v, want %q", field, names[field], expected)
		}
	}
	return nil
}

func normalizeIdentity(crd map[string]any, want identity) error {
	metadata, ok := crd["metadata"].(map[string]any)
	if !ok {
		return fmt.Errorf("metadata is missing")
	}
	spec, ok := crd["spec"].(map[string]any)
	if !ok {
		return fmt.Errorf("spec is missing")
	}
	names, ok := spec["names"].(map[string]any)
	if !ok {
		return fmt.Errorf("spec.names is missing")
	}
	metadata["name"] = want.crdName
	spec["group"] = "kubefacet.steeltanuki.it"
	names["kind"] = want.kind
	names["listKind"] = want.listKind
	names["plural"] = want.plural
	names["singular"] = want.singular
	normalizeDescriptions(crd)
	return nil
}

func normalizeDescriptions(value any) {
	switch current := value.(type) {
	case map[string]any:
		for key, nested := range current {
			if key == "description" {
				if _, ok := nested.(string); ok {
					current[key] = "<descriptive prose>"
				}
				continue
			}
			normalizeDescriptions(nested)
		}
	case []any:
		for _, nested := range current {
			normalizeDescriptions(nested)
		}
	}
}

func valueAt(values map[string]any, key string) any {
	if values == nil {
		return nil
	}
	return values[key]
}

func verifyScheme() error {
	scheme := runtime.NewScheme()
	if err := v1alpha1.AddToScheme(scheme); err != nil {
		return fmt.Errorf("register API scheme: %w", err)
	}
	apiPackage := reflect.TypeOf(v1alpha1.Facet{}).PkgPath()
	registered := make(map[string]bool)
	for gvk, objectType := range scheme.AllKnownTypes() {
		if objectType.PkgPath() != apiPackage {
			continue
		}
		if gvk.Group != v1alpha1.GroupVersion.Group || gvk.Version != v1alpha1.GroupVersion.Version {
			return fmt.Errorf("API type registered under unexpected group/version: %s", gvk)
		}
		registered[gvk.Kind] = true
	}
	want := map[string]bool{"Facet": true, "FacetList": true, "FacetAccessPolicy": true, "FacetAccessPolicyList": true}
	if !reflect.DeepEqual(registered, want) {
		return fmt.Errorf("API scheme types = %v, want %v", registered, want)
	}
	return nil
}
