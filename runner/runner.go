package kcriffrunner

import (
	"github.com/sbug51/kc-riff/api"   // kcriff API
	"github.com/sbug51/kc-riff/llama" // kcriff LLM execution
)

func Execute(args []string) error {
	if args[0] == "runner" {
		args = args[1:]
	}

	var useNewEngine bool
	if args[0] == "--kcriff-engine" { // Change to kcriff
		args = args[1:]
		useNewEngine = true
	}

	if useNewEngine {
		return api.Execute(args) // kcriff API execution
	} else {
		return llama.Execute(args) // kcriff LLM execution
	}
}
