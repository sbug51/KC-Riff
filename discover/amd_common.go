package discover

import (
	"errors"
	"log/slog"
	"os"
	"path/filepath"
	"runtime"
)

func commonAMDValidateLibDir() (string, error) {
	if runtime.GOOS == "windows" {
		// Since ROCm is not supported on Windows, return an error or empty value.
		slog.Warn("ROCm library discovery skipped on Windows; please use CUDA or oneAPI.")
		return "", errors.New("ROCm not supported on Windows")
	}

	// Favor our bundled version

	// Installer payload location if we're running the installed binary
	rocmTargetDir := filepath.Join(Libkc-riffPath, "rocm")
	if rocmLibUsable(rocmTargetDir) {
		slog.Debug("detected ROCM next to kc-riff executable " + rocmTargetDir)
		return rocmTargetDir, nil
	}

	// Prefer explicit HIP env var
	hipPath := os.Getenv("HIP_PATH")
	if hipPath != "" {
		hipLibDir := filepath.Join(hipPath, "bin")
		if rocmLibUsable(hipLibDir) {
			slog.Debug("detected ROCM via HIP_PATH=" + hipPath)
			return hipLibDir, nil
		}
	}

	// Scan the LD_LIBRARY_PATH or PATH
	pathEnv := "LD_LIBRARY_PATH"
	if runtime.GOOS == "windows" {
		pathEnv = "PATH"
	}

	paths := os.Getenv(pathEnv)
	for _, path := range filepath.SplitList(paths) {
		d, err := filepath.Abs(path)
		if err != nil {
			continue
		}
		if rocmLibUsable(d) {
			return d, nil
		}
	}

	// Well known location(s)
	for _, path := range RocmStandardLocations {
		if rocmLibUsable(path) {
			return path, nil
		}
	}

	return "", errors.New("no suitable ROCm found, falling back to CPU")
}
