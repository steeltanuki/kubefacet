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

package v1alpha1

import (
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/types"
)

// Facet is the root custom resource for declarative Kubernetes observation.
//
// +kubebuilder:object:root=true
// +kubebuilder:resource:path=facets,singular=facet,scope=Namespaced
// +kubebuilder:subresource:status
// +kubebuilder:storageversion
type Facet struct {
	metav1.TypeMeta   `json:",inline"`
	metav1.ObjectMeta `json:"metadata,omitempty"`

	// +kubebuilder:validation:Required
	Spec   FacetSpec   `json:"spec"`
	Status FacetStatus `json:"status,omitempty"`
}

// FacetList contains a list of Facet resources.
//
// +kubebuilder:object:root=true
type FacetList struct {
	metav1.TypeMeta `json:",inline"`
	metav1.ListMeta `json:"metadata,omitempty"`
	Items           []Facet `json:"items"`
}

// FacetSpec contains the stable foundation envelope for future sources.
type FacetSpec struct {
	// +optional
	// +listType=map
	// +listMapKey=id
	// +kubebuilder:validation:MaxItems=32
	Sources []FacetSource `json:"sources,omitempty"`
}

// FacetSource identifies one Kubernetes resource selection without granting
// permissions or embedding installation-policy configuration.
type FacetSource struct {
	// +kubebuilder:validation:Required
	// +kubebuilder:validation:MaxLength=63
	// +kubebuilder:validation:Pattern=`^[a-z0-9]([-a-z0-9]*[a-z0-9])?$`
	ID string `json:"id"`

	// +kubebuilder:validation:Required
	Resource ResourceReference `json:"resource"`

	// A nil pointer means the containing Facet namespace for namespaced
	// resources; a non-nil empty Names list intentionally selects no namespace.
	// +optional
	Namespaces *NamespaceSelection `json:"namespaces,omitempty"`

	// +optional
	Selector *ResourceSelector `json:"selector,omitempty"`

	// +optional
	// +listType=map
	// +listMapKey=name
	// +kubebuilder:validation:MaxItems=64
	Fields []FacetField `json:"fields,omitempty"`

	// +optional
	// +listType=map
	// +listMapKey=name
	// +kubebuilder:validation:MaxItems=32
	Aggregations []FacetAggregation `json:"aggregations,omitempty"`
}

// FacetAggregationFunction identifies one supported source-wide reducer.
// +kubebuilder:validation:Enum=collect;count;sum;min;max;average;first;last;distinct
type FacetAggregationFunction string

const (
	AggregationCollect  FacetAggregationFunction = "collect"
	AggregationCount    FacetAggregationFunction = "count"
	AggregationSum      FacetAggregationFunction = "sum"
	AggregationMin      FacetAggregationFunction = "min"
	AggregationMax      FacetAggregationFunction = "max"
	AggregationAverage  FacetAggregationFunction = "average"
	AggregationFirst    FacetAggregationFunction = "first"
	AggregationLast     FacetAggregationFunction = "last"
	AggregationDistinct FacetAggregationFunction = "distinct"
)

// FacetRoundingMode identifies the closed set of average rounding rules.
// +kubebuilder:validation:Enum=halfEven;halfAwayFromZero;towardZero;awayFromZero
type FacetRoundingMode string

const (
	RoundingHalfEven         FacetRoundingMode = "halfEven"
	RoundingHalfAwayFromZero FacetRoundingMode = "halfAwayFromZero"
	RoundingTowardZero       FacetRoundingMode = "towardZero"
	RoundingAwayFromZero     FacetRoundingMode = "awayFromZero"
)

// FacetAggregation declares one typed reduction over the containing
// source's extracted field outcomes. Average options are resolved at runtime
// so omission remains distinguishable from invalid options on other functions.
type FacetAggregation struct {
	// +kubebuilder:validation:Required
	// +kubebuilder:validation:MaxLength=63
	// +kubebuilder:validation:Pattern=`^[a-z][A-Za-z0-9]*(?:-[a-z0-9]+)*$`
	Name string `json:"name"`

	// +kubebuilder:validation:Required
	Function FacetAggregationFunction `json:"function"`

	// +kubebuilder:validation:Required
	// +kubebuilder:validation:MaxLength=63
	// +kubebuilder:validation:Pattern=`^[a-z][A-Za-z0-9]*(?:-[a-z0-9]+)*$`
	Field string `json:"field"`

	// +optional
	// +listType=atomic
	// +kubebuilder:validation:MaxItems=16
	GroupBy []string `json:"groupBy,omitempty"`

	// +optional
	IncludeProvenance bool `json:"includeProvenance,omitempty"`

	// +optional
	// +kubebuilder:validation:Minimum=0
	// +kubebuilder:validation:Maximum=18
	Precision *int32 `json:"precision,omitempty"`

	// +optional
	RoundingMode FacetRoundingMode `json:"roundingMode,omitempty"`
}

// FacetField declares one named native-value extraction from a selected
// resource.
type FacetField struct {
	// +kubebuilder:validation:Required
	// +kubebuilder:validation:MaxLength=63
	// +kubebuilder:validation:Pattern=`^[a-z][A-Za-z0-9]*(?:-[a-z0-9]+)*$`
	Name string `json:"name"`

	// +kubebuilder:validation:Required
	// +kubebuilder:validation:MinLength=1
	// +kubebuilder:validation:MaxLength=1024
	Path string `json:"path"`

	// Type is optional for API compatibility with untyped field declarations.
	// Typed conversion reports a field-scoped missing-type failure when it is
	// omitted.
	// +optional
	Type FacetValueType `json:"type,omitempty"`

	// +optional
	// +listType=atomic
	// +kubebuilder:validation:MaxItems=16
	Operators []FacetOperator `json:"operators,omitempty"`
}

// FacetValueType identifies the explicit logical type requested for one
// extracted field.
// +kubebuilder:validation:Enum=string;integer;number;boolean;timestamp;duration;quantity;object;list
type FacetValueType string

const (
	ValueTypeString    FacetValueType = "string"
	ValueTypeInteger   FacetValueType = "integer"
	ValueTypeNumber    FacetValueType = "number"
	ValueTypeBoolean   FacetValueType = "boolean"
	ValueTypeTimestamp FacetValueType = "timestamp"
	ValueTypeDuration  FacetValueType = "duration"
	ValueTypeQuantity  FacetValueType = "quantity"
	ValueTypeObject    FacetValueType = "object"
	ValueTypeList      FacetValueType = "list"
)

// FacetOperatorName identifies one supported field operator.
// +kubebuilder:validation:Enum=eq;ne;gt;gte;lt;lte;contains;startsWith;endsWith;matches;exists;notExists;in;notIn;default;coalesce
type FacetOperatorName string

const (
	OperatorEq         FacetOperatorName = "eq"
	OperatorNe         FacetOperatorName = "ne"
	OperatorGt         FacetOperatorName = "gt"
	OperatorGte        FacetOperatorName = "gte"
	OperatorLt         FacetOperatorName = "lt"
	OperatorLte        FacetOperatorName = "lte"
	OperatorContains   FacetOperatorName = "contains"
	OperatorStartsWith FacetOperatorName = "startsWith"
	OperatorEndsWith   FacetOperatorName = "endsWith"
	OperatorMatches    FacetOperatorName = "matches"
	OperatorExists     FacetOperatorName = "exists"
	OperatorNotExists  FacetOperatorName = "notExists"
	OperatorIn         FacetOperatorName = "in"
	OperatorNotIn      FacetOperatorName = "notIn"
	OperatorDefault    FacetOperatorName = "default"
	OperatorCoalesce   FacetOperatorName = "coalesce"
)

// FacetOperator declares one ordered operation over a typed field.
type FacetOperator struct {
	// +kubebuilder:validation:Required
	Operator FacetOperatorName `json:"operator"`

	// +optional
	Value *FacetOperatorOperand `json:"value,omitempty"`

	// +optional
	// +listType=atomic
	// +kubebuilder:validation:MaxItems=128
	Values []FacetOperatorOperand `json:"values,omitempty"`
}

// FacetOperatorOperand is a structural typed operand. Exactly one payload
// branch is valid when State is MatchStateValue; MatchStateNull is rejected by
// runtime operator planning and exists to keep an explicit null distinct from
// an omitted operand.
type FacetOperatorOperand struct {
	// +kubebuilder:validation:Required
	State FacetMatchState `json:"state"`

	// +optional
	StringValue *string `json:"stringValue,omitempty"`

	// +optional
	IntegerValue *int64 `json:"integerValue,omitempty"`

	// +optional
	NumberValue *string `json:"numberValue,omitempty"`

	// +optional
	BooleanValue *bool `json:"booleanValue,omitempty"`

	// +optional
	TimestampValue *string `json:"timestampValue,omitempty"`

	// +optional
	DurationValue *string `json:"durationValue,omitempty"`

	// +optional
	QuantityValue *string `json:"quantityValue,omitempty"`

	// +optional
	ObjectValue *string `json:"objectValue,omitempty"`

	// +optional
	ListValue *string `json:"listValue,omitempty"`
}

// ResourceReference identifies the API version and Kind resolved through
// Kubernetes discovery.
type ResourceReference struct {
	// +kubebuilder:validation:Required
	// +kubebuilder:validation:MinLength=1
	APIVersion string `json:"apiVersion"`

	// +kubebuilder:validation:Required
	// +kubebuilder:validation:MinLength=1
	Kind string `json:"kind"`
}

// NamespaceSelection narrows a namespaced source to an explicit namespace set.
// Names intentionally omits omitempty so an explicit empty list remains
// distinguishable from an omitted namespace block after serialization.
type NamespaceSelection struct {
	// +listType=set
	// +kubebuilder:validation:MaxItems=64
	// +kubebuilder:validation:items:MaxLength=63
	// +kubebuilder:validation:items:Pattern=`^[a-z0-9]([-a-z0-9]*[a-z0-9])?$`
	Names []string `json:"names"`
}

// ResourceSelector expresses Kubernetes-native name, label, and field
// selection constraints. All populated mechanisms are combined by the
// selection planner.
type ResourceSelector struct {
	// +optional
	Name string `json:"name,omitempty"`

	// +optional
	// +kubebuilder:validation:MaxProperties=64
	MatchLabels map[string]string `json:"matchLabels,omitempty"`

	// +optional
	// +listType=atomic
	// +kubebuilder:validation:MaxItems=64
	MatchExpressions []metav1.LabelSelectorRequirement `json:"matchExpressions,omitempty"`

	// +optional
	FieldSelector string `json:"fieldSelector,omitempty"`
}

// FacetStatus contains controller-observed state for a Facet resource.
type FacetStatus struct {
	// +optional
	// +kubebuilder:validation:Minimum=0
	ObservedGeneration int64 `json:"observedGeneration,omitempty"`

	// +optional
	// +listType=map
	// +listMapKey=type
	Conditions []metav1.Condition `json:"conditions,omitempty"`

	// +optional
	Summary *FacetSummary `json:"summary,omitempty"`

	// +optional
	// +kubebuilder:validation:MaxLength=71
	// +kubebuilder:validation:Pattern=`^sha256:[0-9a-f]{64}$`
	ResultHash string `json:"resultHash,omitempty"`

	// +optional
	Result *FacetResult `json:"result,omitempty"`
}

// FacetSummary contains compact counts derived from the structural result.
type FacetSummary struct {
	// +kubebuilder:validation:Minimum=0
	SuccessfulSources int64 `json:"successfulSources"`

	// +kubebuilder:validation:Minimum=0
	FailedSources int64 `json:"failedSources"`

	// +kubebuilder:validation:Minimum=0
	MatchedResources int64 `json:"matchedResources"`
}

// FacetResult is the structural, ordered typed-output snapshot published
// in status.
type FacetResult struct {
	// +optional
	// +listType=atomic
	Sources []FacetSourceResult `json:"sources,omitempty"`
}

// FacetSourceState identifies whether a source produced values or failed.
// +kubebuilder:validation:Enum=values;error
type FacetSourceState string

const (
	SourceStateValues FacetSourceState = "values"
	SourceStateError  FacetSourceState = "error"
)

// FacetFieldState identifies absence, values, or a field-scoped failure.
// +kubebuilder:validation:Enum=absent;values;error
type FacetFieldState string

const (
	FieldStateAbsent FacetFieldState = "absent"
	FieldStateValues FacetFieldState = "values"
	FieldStateError  FacetFieldState = "error"
)

// FacetMatchState distinguishes a non-null value from an explicit null.
// +kubebuilder:validation:Enum=value;null
type FacetMatchState string

const (
	MatchStateValue FacetMatchState = "value"
	MatchStateNull  FacetMatchState = "null"
)

// FacetSourceResult is one source-scoped typed-output result.
type FacetSourceResult struct {
	// +kubebuilder:validation:Required
	ID string `json:"id"`

	// +kubebuilder:validation:Required
	State FacetSourceState `json:"state"`

	// +optional
	// +listType=atomic
	FieldErrors []FacetFieldError `json:"fieldErrors,omitempty"`

	// +optional
	// +listType=atomic
	Resources []FacetResourceResult `json:"resources,omitempty"`

	// +optional
	// +listType=atomic
	Aggregates []FacetAggregateResult `json:"aggregates,omitempty"`

	// +optional
	Error *FacetResultError `json:"error,omitempty"`
}

// FacetAggregateState identifies the terminal state of one aggregate.
// +kubebuilder:validation:Enum=values;degraded;error
type FacetAggregateState string

const (
	AggregateStateValues   FacetAggregateState = "values"
	AggregateStateDegraded FacetAggregateState = "degraded"
	AggregateStateError    FacetAggregateState = "error"
)

// FacetAggregateValueState distinguishes an absent scalar from a value
// collection, including an intentionally empty collection.
// +kubebuilder:validation:Enum=absent;values
type FacetAggregateValueState string

const (
	AggregateValueAbsent FacetAggregateValueState = "absent"
	AggregateValueValues FacetAggregateValueState = "values"
)

// FacetAggregateResult is one source-scoped aggregate outcome.
type FacetAggregateResult struct {
	// +kubebuilder:validation:Required
	Name string `json:"name"`

	// +kubebuilder:validation:Required
	Function FacetAggregationFunction `json:"function"`

	// +kubebuilder:validation:Required
	Field string `json:"field"`

	// +kubebuilder:validation:Required
	State FacetAggregateState `json:"state"`

	// +optional
	// +listType=atomic
	Groups []FacetAggregateGroup `json:"groups,omitempty"`

	// +optional
	// +listType=atomic
	Failures []FacetAggregateResourceFailure `json:"failures,omitempty"`

	// +optional
	Error *FacetResultError `json:"error,omitempty"`
}

// FacetAggregateKey is one ordered typed group-key component.
type FacetAggregateKey struct {
	// +kubebuilder:validation:Required
	Field string `json:"field"`

	// +kubebuilder:validation:Required
	Type FacetValueType `json:"type"`

	// +kubebuilder:validation:Required
	Value FacetTypedMatch `json:"value"`
}

// FacetAggregateGroup is one ordered key and reduced value.
type FacetAggregateGroup struct {
	// +optional
	// +listType=atomic
	Keys []FacetAggregateKey `json:"keys,omitempty"`

	// +kubebuilder:validation:Required
	Value FacetAggregateValue `json:"value"`

	// +optional
	// +listType=atomic
	Contributors []FacetResourceProvenance `json:"contributors,omitempty"`
}

// FacetAggregateValue is a typed scalar or collection result.
type FacetAggregateValue struct {
	// +kubebuilder:validation:Required
	Type FacetValueType `json:"type"`

	// +kubebuilder:validation:Required
	State FacetAggregateValueState `json:"state"`

	// +optional
	// +listType=atomic
	Matches []FacetAggregateMatch `json:"matches,omitempty"`
}

// FacetAggregateMatch is one typed aggregate value and optional
// value-specific provenance.
type FacetAggregateMatch struct {
	// +kubebuilder:validation:Required
	Value FacetTypedMatch `json:"value"`

	// +optional
	// +listType=atomic
	Contributors []FacetResourceProvenance `json:"contributors,omitempty"`
}

// FacetResourceProvenance identifies one contributing Kubernetes resource.
type FacetResourceProvenance struct {
	// +kubebuilder:validation:Required
	APIVersion string `json:"apiVersion"`

	// +kubebuilder:validation:Required
	Kind string `json:"kind"`

	// +optional
	Namespace string `json:"namespace,omitempty"`

	// +kubebuilder:validation:Required
	Name string `json:"name"`

	// +kubebuilder:validation:Required
	UID types.UID `json:"uid"`
}

// FacetAggregateResourceFailure associates a sanitized failure with the
// resource whose contribution could not be evaluated.
type FacetAggregateResourceFailure struct {
	// +kubebuilder:validation:Required
	Provenance FacetResourceProvenance `json:"provenance"`

	// +kubebuilder:validation:Required
	Error FacetResultError `json:"error"`
}

// FacetResourceResult identifies one contributing selected resource and
// its ordered typed fields.
type FacetResourceResult struct {
	// +kubebuilder:validation:Required
	APIVersion string `json:"apiVersion"`

	// +kubebuilder:validation:Required
	Kind string `json:"kind"`

	// +optional
	Namespace string `json:"namespace,omitempty"`

	// +kubebuilder:validation:Required
	Name string `json:"name"`

	// +kubebuilder:validation:Required
	UID types.UID `json:"uid"`

	// +optional
	// +listType=atomic
	Fields []FacetFieldResult `json:"fields,omitempty"`

	// +optional
	Error *FacetResultError `json:"error,omitempty"`
}

// FacetFieldResult is one field-scoped typed outcome.
type FacetFieldResult struct {
	// +kubebuilder:validation:Required
	Name string `json:"name"`

	// +optional
	Type FacetValueType `json:"type,omitempty"`

	// +kubebuilder:validation:Required
	State FacetFieldState `json:"state"`

	// +optional
	// +listType=atomic
	Matches []FacetTypedMatch `json:"matches,omitempty"`

	// +optional
	Error *FacetResultError `json:"error,omitempty"`
}

// FacetTypedMatch is one ordered typed match. Exactly one typed payload is
// populated when State is value; all payloads are omitted for null.
type FacetTypedMatch struct {
	// +kubebuilder:validation:Required
	State FacetMatchState `json:"state"`

	// +optional
	StringValue *string `json:"stringValue,omitempty"`

	// +optional
	IntegerValue *int64 `json:"integerValue,omitempty"`

	// +optional
	NumberValue *string `json:"numberValue,omitempty"`

	// +optional
	BooleanValue *bool `json:"booleanValue,omitempty"`

	// +optional
	TimestampValue *metav1.Time `json:"timestampValue,omitempty"`

	// +optional
	DurationValue *FacetDurationValue `json:"durationValue,omitempty"`

	// +optional
	QuantityValue *FacetQuantityValue `json:"quantityValue,omitempty"`

	// +optional
	ObjectValue *string `json:"objectValue,omitempty"`

	// +optional
	ListValue *string `json:"listValue,omitempty"`
}

// FacetDurationValue is the canonical duration text and exact nanosecond
// magnitude.
type FacetDurationValue struct {
	// +kubebuilder:validation:Required
	Canonical string `json:"canonical"`

	// +kubebuilder:validation:Required
	Nanoseconds int64 `json:"nanoseconds"`
}

// FacetQuantityValue is the canonical Kubernetes quantity text and exact
// normalized base-unit decimal magnitude.
type FacetQuantityValue struct {
	// +kubebuilder:validation:Required
	Canonical string `json:"canonical"`

	// +kubebuilder:validation:Required
	BaseUnits string `json:"baseUnits"`
}

// FacetFieldError is a sanitized field planning failure.
type FacetFieldError struct {
	// +kubebuilder:validation:Required
	Name string `json:"name"`

	// +kubebuilder:validation:Required
	Reason string `json:"reason"`

	// +optional
	Message string `json:"message,omitempty"`
}

// FacetResultError is a sanitized runtime or source-level failure.
type FacetResultError struct {
	// +kubebuilder:validation:Required
	Reason string `json:"reason"`

	// +optional
	Message string `json:"message,omitempty"`
}
