//go:build linux || windows
// +build linux windows

package discover

import (
	"log/slog"
	"os"
	"regexp"
	"runtime"
	"strconv"
	"strings"
)

// Jetson devices have JETSON_JETPACK="x.y.z" factory set to the Jetpack version installed.
// This is only applicable on Linux; on Windows, it will be ignored.
var CudaTegra string = os.Getenv("JETSON_JETPACK")

// cudaGetVisibleDevicesEnv returns the environment variable and value for visible CUDA devices.
func cudaGetVisibleDevicesEnv(gpuInfo []GpuInfo) (string, string) {
	ids := []string{}
	for _, info := range gpuInfo {
		if info.Library != "cuda" {
			// This should not happen if things are wired correctly...
			slog.Debug("cudaGetVisibleDevicesEnv skipping over non-cuda device", "library", info.Library)
			continue
		}
		ids = append(ids, info.ID)
	}
	return "CUDA_VISIBLE_DEVICES", strings.Join(ids, ",")
}

// cudaVariant returns a string representing the CUDA variant to use.
// On Windows, Jetson-specific logic is skipped.
func cudaVariant(gpuInfo CudaGPUInfo) string {
	if runtime.GOOS == "windows" {
		// For Windows, we rely solely on compute capability and driver versions.
		if gpuInfo.computeMajor < 6 || gpuInfo.DriverMajor < 12 || (gpuInfo.DriverMajor == 12 && gpuInfo.DriverMinor == 0) {
			return "v11"
		}
		return "v12"
	}

	// For Linux on ARM (Jetson), check for Jetson-specific environment variables.
	if runtime.GOARCH == "arm64" && runtime.GOOS == "linux" {
		if CudaTegra != "" {
			ver := strings.Split(CudaTegra, ".")
			if len(ver) > 0 {
				return "jetpack" + ver[0]
			}
		} else if data, err := os.ReadFile("/etc/nv_tegra_release"); err == nil {
			r := regexp.MustCompile(` R(\d+) `)
			m := r.FindSubmatch(data)
			if len(m) != 2 {
				slog.Info("Unexpected format for /etc/nv_tegra_release. Set JETSON_JETPACK to select version")
			} else {
				if l4t, err := strconv.Atoi(string(m[1])); err == nil {
					switch l4t {
					case 35:
						return "jetpack5"
					case 36:
						return "jetpack6"
					default:
						slog.Info("unsupported L4T version", "nv_tegra_release", string(data))
					}
				}
			}
		}
	}

	// Default logic for non-Jetson devices.
	if gpuInfo.computeMajor < 6 || gpuInfo.DriverMajor < 12 || (gpuInfo.DriverMajor == 12 && gpuInfo.DriverMinor == 0) {
		return "v11"
	}
	return "v12"
}
