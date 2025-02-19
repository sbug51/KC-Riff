// Package errtypes contains custom error types
package errtypes

import (
	"fmt"
	"strings"
)

const (
	UnknownkcriffKeyErrMsg = "unknown kcriff key"
	InvalidModelNameErrMsg = "invalid model name"
)

// TODO: This should have a structured response from the API
type UnknownkcriffKey struct {
	Key string
}

func (e *UnknownkcriffKey) Error() string {
	return fmt.Sprintf("unauthorized: %s %q", UnknownkcriffKeyErrMsg, strings.TrimSpace(e.Key))
}
