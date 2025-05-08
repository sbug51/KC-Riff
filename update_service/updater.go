package updateservice

import (
	"encoding/json"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"time"
)

// UpdateInfo represents information about an available update
type UpdateInfo struct {
	Available      bool      `json:"available"`
	CurrentVersion string    `json:"current_version"`
	NewVersion     string    `json:"new_version"`
	ReleaseDate    time.Time `json:"release_date"`
	ReleaseNotes   string    `json:"release_notes"`
	DownloadURL    string    `json:"download_url,omitempty"`
}

// UpdateManager handles checking for and applying updates
type UpdateManager struct {
	dataDir        string
	currentVersion string
	lastCheck      time.Time
	updateInfo     *UpdateInfo
}

// New creates a new UpdateManager instance
func New(dataDir string, currentVersion string) (*UpdateManager, error) {
	// Create data directory if it doesn't exist
	if err := os.MkdirAll(dataDir, 0755); err != nil {
		return nil, fmt.Errorf("failed to create data directory: %w", err)
	}

	return &UpdateManager{
		dataDir:        dataDir,
		currentVersion: currentVersion,
	}, nil
}

// CheckForUpdates checks if an update is available
// In a real implementation, this would contact a server to check for updates
func (um *UpdateManager) CheckForUpdates() (*UpdateInfo, error) {
	// In a real implementation, we would make a network request to check for updates
	// For simulation purposes, we'll return a static response

	// Pretend to do a network request
	time.Sleep(500 * time.Millisecond)

	// Simulate an available update
	um.updateInfo = &UpdateInfo{
		Available:      true,
		CurrentVersion: um.currentVersion,
		NewVersion:     "0.2.0", // Always one version ahead
		ReleaseDate:    time.Now(),
		ReleaseNotes:   "Bug fixes and performance improvements",
		DownloadURL:    "https://example.com/kcriff/update/0.2.0",
	}

	um.lastCheck = time.Now()

	// Save update info to disk
	um.saveUpdateInfo()

	return um.updateInfo, nil
}

// saveUpdateInfo saves the current update info to disk
func (um *UpdateManager) saveUpdateInfo() error {
	if um.updateInfo == nil {
		return nil
	}

	updateInfoPath := filepath.Join(um.dataDir, "update_info.json")
	data, err := json.MarshalIndent(um.updateInfo, "", "  ")
	if err != nil {
		return fmt.Errorf("failed to marshal update info: %w", err)
	}

	if err := os.WriteFile(updateInfoPath, data, 0644); err != nil {
		return fmt.Errorf("failed to write update info to file: %w", err)
	}

	return nil
}

// loadUpdateInfo loads saved update info from disk
func (um *UpdateManager) loadUpdateInfo() error {
	updateInfoPath := filepath.Join(um.dataDir, "update_info.json")
	data, err := os.ReadFile(updateInfoPath)
	if err != nil {
		if os.IsNotExist(err) {
			// No saved update info
			return nil
		}
		return fmt.Errorf("failed to read update info file: %w", err)
	}

	var updateInfo UpdateInfo
	if err := json.Unmarshal(data, &updateInfo); err != nil {
		return fmt.Errorf("failed to parse update info file: %w", err)
	}

	um.updateInfo = &updateInfo
	return nil
}

// GetLastUpdateInfo returns the latest update info without checking for new updates
func (um *UpdateManager) GetLastUpdateInfo() *UpdateInfo {
	if um.updateInfo == nil {
		// Try to load from disk
		if err := um.loadUpdateInfo(); err != nil {
			log.Printf("Warning: Failed to load update info: %v", err)
		}
	}
	return um.updateInfo
}

// ApplyUpdate applies the available update
// In a real implementation, this would download and install the update
func (um *UpdateManager) ApplyUpdate() error {
	if um.updateInfo == nil || !um.updateInfo.Available {
		return fmt.Errorf("no update available to apply")
	}

	// Simulate downloading and applying the update
	log.Printf("Downloading update from %s...", um.updateInfo.DownloadURL)
	time.Sleep(2 * time.Second)
	
	log.Printf("Installing update %s...", um.updateInfo.NewVersion)
	time.Sleep(1 * time.Second)
	
	// Update the current version
	um.currentVersion = um.updateInfo.NewVersion
	
	// Create a new update info that shows no more updates available
	um.updateInfo = &UpdateInfo{
		Available:      false,
		CurrentVersion: um.currentVersion,
		NewVersion:     um.currentVersion,
		ReleaseDate:    time.Now(),
		ReleaseNotes:   "",
	}
	
	// Save the new update info
	um.saveUpdateInfo()
	
	log.Printf("Update to version %s completed successfully!", um.currentVersion)
	return nil
}