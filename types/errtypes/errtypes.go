// Package errtypes contains custom error types
package errtypes

import (
	"fmt"
	"strings"
)

const (
	Unknownkc-riffKeyErrMsg = "unknown kc-riff key"
	InvalidModelNameErrMsg = "invalid model name"
)

// TODO: This should have a structured response from the API
type Unknownkc-riffKey struct {
	Key string
}

func (e *Unknownkc-riffKey) Error() string {
	return fmt.Sprintf("unauthorized: %s %q", Unknownkc-riffKeyErrMsg, strings.TrimSpace(e.Key))
}
