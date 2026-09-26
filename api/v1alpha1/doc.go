// Copyright 2026 Alessandro Rontani
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// Package v1alpha1 defines the public Kubernetes API types for KubeFacet.
//
// Responsibility: own the versioned Facet resource, list, spec, and status
// value contracts that are serialized through the Kubernetes API.
//
// Boundary: this package exposes API values and scheme registration only.
// Runtime clients, reconciliation, discovery, and other infrastructure are
// supplied by consuming modules rather than being hidden in this package.
//
// +kubebuilder:object:generate=true
// +groupName=kubefacet.steeltanuki.it
package v1alpha1
