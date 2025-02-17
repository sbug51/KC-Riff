//go:build linux || windows
// +build linux windows

package discover

import (
	"log/slog"
	"runtime"
	"strings"
)

// oneapiGetVisibleDevicesEnv returns the environment variable and its value
// for selecting oneAPI (Level Zero) devices. On Windows, if needed, you can adjust
// the prefix; for now, we use the same "level_zero:" prefix as on Linux.
func oneapiGetVisibleDevicesEnv(gpuInfo []GpuInfo) (string, string) {
	ids := []string{}
	for _, info := range gpuInfo {
		if info.Library != "oneapi" {
			// This shouldn't happen if things are wired correctly.
			slog.Debug("oneapiGetVisibleDevicesEnv skipping over non-sycl device", "library", info.Library)
			continue
		}
		ids = append(ids, info.ID)
	}

	// Set the prefix for the oneAPI device selector.
	// On Windows, adjust this if necessary.
	prefix := "level_zero:"
	if runtime.GOOS == "windows" {
		// If Windows requires a different prefix, change it here.
		prefix = "level_zero:" // For now, we assume it's the same.
	}

	return "ONEAPI_DEVICE_SELECTOR", prefix + strings.Join(ids, ",")
}
