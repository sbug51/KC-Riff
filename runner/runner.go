package runner

import (
	"github.com/sbug51/KC-Riff/api"   // KC Riff API
	"github.com/sbug51/KC-Riff/llama" // KC Riff LLM execution
)

func Execute(args []string) error {
	if args[0] == "runner" {
		args = args[1:]
	}

	var useNewEngine bool
	if args[0] == "--kc-riff-engine" { // Change to KC Riff
		args = args[1:]
		useNewEngine = true
	}

	if useNewEngine {
		return api.Execute(args) // KC Riff API execution
	} else {
		return llama.Execute(args) // KC Riff LLM execution
	}
}
