# OPA/Rego policy: approve advisory only if the model version AND its
# artifact hash appear in the approved set. Both must match, because a
# signed envelope from a retired model with the current version number
# must still be rejected.
package advisory.model

default allow := false

allow if {
    some approved in data.approved_versions
    approved.version == input.model.version
    approved.artifact_hash == input.model.artifact_hash
}
