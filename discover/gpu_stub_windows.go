//go:build windows
// +build windows

package discover

import (
	"errors"
	"log/slog"
)

// Define stub types to satisfy the function signatures.
// These types can be empty because we’re not actually using GPU functionality on Windows.
type cudart_handle_t struct{}
type nvcuda_handle_t struct{}
type nvml_handle_t struct{}
type oneapi_handle_t struct{}

// Stub implementation of loadCUDARTMgmt.
// Returns zero devices and an error.
func loadCUDARTMgmt(cudartLibPaths []string) (int, *cudart_handle_t, string, error) {
	slog.Info("loadCUDARTMgmt stub: CUDA management not supported on Windows")
	return 0, nil, "", errors.New("CUDA not supported on Windows")
}

// Stub implementation of loadNVCUDAMgmt.
// Returns zero devices and an error.
func loadNVCUDAMgmt(nvcudaLibPaths []string) (int, *nvcuda_handle_t, string, error) {
	slog.Info("loadNVCUDAMgmt stub: NVCUDA management not supported on Windows")
	return 0, nil, "", errors.New("NVCUDA not supported on Windows")
}

// Stub implementation of loadNVMLMgmt.
// Returns nil and an error.
func loadNVMLMgmt(nvmlLibPaths []string) (*nvml_handle_t, string, error) {
	slog.Info("loadNVMLMgmt stub: NVML management not supported on Windows")
	return nil, "", errors.New("NVML not supported on Windows")
}

// Stub implementation of loadOneapiMgmt.
// Returns zero devices and an error.
func loadOneapiMgmt(oneapiLibPaths []string) (int, *oneapi_handle_t, string, error) {
	slog.Info("loadOneapiMgmt stub: oneAPI management not supported on Windows")
	return 0, nil, "", errors.New("oneAPI not supported on Windows")
}
