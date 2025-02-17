//go:build linux || windows
// +build linux windows

package discover

import (
	"errors"
	"log/slog"
	"os"
	"path/filepath"
	"runtime"
	"strings"
)

// rocmLibUsable determines if the given ROCm lib directory is usable by checking for the existence of some glob patterns.
func rocmLibUsable(libDir string) bool {
	slog.Debug("evaluating potential rocm lib dir " + libDir)
	for _, g := range ROCmLibGlobs {
		res, _ := filepath.Glob(filepath.Join(libDir, g))
		if len(res) == 0 {
			return false
		}
	}
	return true
}

// GetSupportedGFX returns a list of supported GFX types from the ROCm library directory.
func GetSupportedGFX(libDir string) ([]string, error) {
	var ret []string
	files, err := filepath.Glob(filepath.Join(libDir, "rocblas", "library", "TensileLibrary_lazy_gfx*.dat"))
	if err != nil {
		return nil, err
	}
	for _, file := range files {
		ret = append(ret, strings.TrimSuffix(strings.TrimPrefix(filepath.Base(file), "TensileLibrary_lazy_"), ".dat"))
	}
	return ret, nil
}

// commonAMDValidateLibDir attempts to locate a valid ROCm library directory.
func commonAMDValidateLibDir() (string, error) {
	// Favor our bundled version

	// Installer payload location if we're running the installed binary
	rocmTargetDir := filepath.Join(LibOllamaPath, "rocm")
	if rocmLibUsable(rocmTargetDir) {
		slog.Debug("detected ROCM next to ollama executable " + rocmTargetDir)
		return rocmTargetDir, nil
	}

	// Prefer explicit HIP env var
	hipPath :
