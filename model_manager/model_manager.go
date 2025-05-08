package modelmanager

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"os"
	"path/filepath"
	"sync"
	"time"
)

// Model represents an AI model available for download and use
type Model struct {
	Name          string   `json:"name"`
	Description   string   `json:"description"`
	Size          int64    `json:"size"`
	Parameters    int64    `json:"parameters"`
	Category      string   `json:"category"`
	Tags          []string `json:"tags"`
	IsDownloaded  bool     `json:"downloaded"`
	KCRecommended bool     `json:"kc_recommended"`
	FilePath      string   `json:"file_path,omitempty"`
}

// DownloadStatus represents the current status of a model download
type DownloadStatus struct {
	ModelName  string  `json:"model_name"`
	Progress   float64 `json:"progress"`
	Status     string  `json:"status"`
	Error      string  `json:"error,omitempty"`
	Completed  bool    `json:"completed"`
	Downloaded int64   `json:"downloaded_bytes"`
	TotalSize  int64   `json:"total_bytes"`
}

// ModelManager handles model discovery, downloading, and management
type ModelManager struct {
	modelsDir    string
	models       []Model
	downloads    map[string]*DownloadStatus
	downloadLock sync.Mutex
	cancelDownload map[string]bool
}

// New creates a new ModelManager instance
func New(modelsDir string) (*ModelManager, error) {
	// Create models directory if it doesn't exist
	if err := os.MkdirAll(modelsDir, 0755); err != nil {
		return nil, fmt.Errorf("failed to create models directory: %w", err)
	}

	mm := &ModelManager{
		modelsDir:      modelsDir,
		downloads:      make(map[string]*DownloadStatus),
		cancelDownload: make(map[string]bool),
	}

	// Load initial models (in a real implementation, this would fetch from a server or local database)
	mm.loadInitialModels()

	// Update download status of existing models
	mm.refreshDownloadStatus()

	return mm, nil
}

// loadInitialModels loads the initial set of models
// In a real implementation, this would likely fetch models from a server
func (mm *ModelManager) loadInitialModels() {
	// These are example models - in a real implementation, we would fetch this list
	// from a remote server or local database
	mm.models = []Model{
		{
			Name:          "mistral-7b",
			Description:   "Mistral 7B is a powerful general-purpose language model with 7.3B parameters",
			Size:          4500000000,
			Parameters:    7000000000,
			Tags:          []string{"language", "general", "chat"},
			Category:      "recommended",
			IsDownloaded:  false,
			KCRecommended: true,
		},
		{
			Name:          "llava",
			Description:   "LLaVA (Large Language and Vision Assistant) is a multimodal model for visual understanding",
			Size:          4200000000,
			Parameters:    7000000000,
			Tags:          []string{"multimodal", "vision", "chat"},
			Category:      "recommended",
			IsDownloaded:  false,
			KCRecommended: true,
		},
		{
			Name:          "moondream",
			Description:   "Moondream is optimized for vision tasks",
			Size:          1200000000,
			Parameters:    1500000000,
			Tags:          []string{"vision", "efficient"},
			Category:      "recommended",
			IsDownloaded:  false,
			KCRecommended: true,
		},
		{
			Name:          "stablelm",
			Description:   "StableLM is a lightweight model focused on stability for long-term deployment",
			Size:          3200000000,
			Parameters:    3000000000,
			Tags:          []string{"stable", "general", "efficient"},
			Category:      "general",
			IsDownloaded:  false,
			KCRecommended: false,
		},
		{
			Name:          "phi-2",
			Description:   "Phi-2 is a compact model with excellent reasoning capabilities",
			Size:          2500000000,
			Parameters:    2700000000,
			Tags:          []string{"reasoning", "efficient", "small"},
			Category:      "general",
			IsDownloaded:  false,
			KCRecommended: false,
		},
	}
}

// refreshDownloadStatus checks if the models are already downloaded
func (mm *ModelManager) refreshDownloadStatus() {
	for i, model := range mm.models {
		// Check if the model file exists in the models directory
		modelPath := filepath.Join(mm.modelsDir, model.Name+".bin")
		_, err := os.Stat(modelPath)
		if err == nil {
			// Model exists, mark as downloaded
			mm.models[i].IsDownloaded = true
			mm.models[i].FilePath = modelPath
		}
	}
}

// GetModels returns the current list of available models
func (mm *ModelManager) GetModels() []Model {
	return mm.models
}

// GetRecommendedModels returns only the recommended models
func (mm *ModelManager) GetRecommendedModels() []Model {
	var recommended []Model
	for _, model := range mm.models {
		if model.KCRecommended {
			recommended = append(recommended, model)
		}
	}
	return recommended
}

// GetDownloadedModels returns only the downloaded models
func (mm *ModelManager) GetDownloadedModels() []Model {
	var downloaded []Model
	for _, model := range mm.models {
		if model.IsDownloaded {
			downloaded = append(downloaded, model)
		}
	}
	return downloaded
}

// StartModelDownload begins the download process for a model
func (mm *ModelManager) StartModelDownload(modelName string) (*DownloadStatus, error) {
	// Find the model
	var modelToDownload *Model
	for i, model := range mm.models {
		if model.Name == modelName {
			modelToDownload = &mm.models[i]
			break
		}
	}

	if modelToDownload == nil {
		return nil, fmt.Errorf("model not found: %s", modelName)
	}

	// Check if already downloaded
	if modelToDownload.IsDownloaded {
		status := &DownloadStatus{
			ModelName:  modelName,
			Progress:   100,
			Status:     "completed",
			Completed:  true,
			Downloaded: modelToDownload.Size,
			TotalSize:  modelToDownload.Size,
		}
		return status, nil
	}

	// Check if already downloading
	mm.downloadLock.Lock()
	defer mm.downloadLock.Unlock()

	existingStatus, exists := mm.downloads[modelName]
	if exists {
		return existingStatus, nil
	}

	// Create new download status
	status := &DownloadStatus{
		ModelName:  modelName,
		Progress:   0,
		Status:     "downloading",
		Completed:  false,
		Downloaded: 0,
		TotalSize:  modelToDownload.Size,
	}
	mm.downloads[modelName] = status
	mm.cancelDownload[modelName] = false

	// Start download in background
	go mm.downloadModel(modelName, modelToDownload.Size)

	return status, nil
}

// GetDownloadStatus returns the current download status for a model
func (mm *ModelManager) GetDownloadStatus(modelName string) (*DownloadStatus, error) {
	// Check if model exists
	var modelExists bool
	for _, model := range mm.models {
		if model.Name == modelName {
			modelExists = true
			if model.IsDownloaded {
				// Model is already downloaded
				return &DownloadStatus{
					ModelName:  modelName,
					Progress:   100,
					Status:     "completed",
					Completed:  true,
					Downloaded: model.Size,
					TotalSize:  model.Size,
				}, nil
			}
			break
		}
	}

	if !modelExists {
		return nil, fmt.Errorf("model not found: %s", modelName)
	}

	// Check if currently downloading
	mm.downloadLock.Lock()
	defer mm.downloadLock.Unlock()

	status, exists := mm.downloads[modelName]
	if !exists {
		// Not downloaded and not in progress
		return &DownloadStatus{
			ModelName: modelName,
			Progress:  0,
			Status:    "not_started",
			Completed: false,
		}, nil
	}

	return status, nil
}

// downloadModel simulates downloading a model
// In a real implementation, this would use HTTP requests to download from a server
func (mm *ModelManager) downloadModel(modelName string, totalSize int64) {
	// Get model target path
	modelPath := filepath.Join(mm.modelsDir, modelName+".bin")

	// Create output file
	outFile, err := os.Create(modelPath)
	if err != nil {
		mm.downloadLock.Lock()
		status := mm.downloads[modelName]
		status.Status = "failed"
		status.Error = fmt.Sprintf("Failed to create output file: %s", err)
		status.Completed = true
		mm.downloadLock.Unlock()
		return
	}
	defer outFile.Close()

	// Simulate chunked download
	totalChunks := 20
	chunkSize := totalSize / int64(totalChunks)
	chunk := make([]byte, chunkSize)

	for i := 1; i <= totalChunks; i++ {
		// Check if we should cancel
		mm.downloadLock.Lock()
		if mm.cancelDownload[modelName] {
			// Cleanup the partial file
			outFile.Close()
			os.Remove(modelPath)
			
			status := mm.downloads[modelName]
			status.Status = "cancelled"
			status.Completed = true
			mm.downloadLock.Unlock()
			
			log.Printf("Download of model %s cancelled\n", modelName)
			return
		}
		mm.downloadLock.Unlock()

		// Simulate network delay
		time.Sleep(300 * time.Millisecond)

		// Fill the chunk with random data
		for j := range chunk {
			chunk[j] = byte(j % 256)
		}

		// Write chunk to file
		_, err := outFile.Write(chunk)
		if err != nil {
			mm.downloadLock.Lock()
			status := mm.downloads[modelName]
			status.Status = "failed"
			status.Error = fmt.Sprintf("Failed to write chunk: %s", err)
			status.Completed = true
			mm.downloadLock.Unlock()
			
			// Cleanup the partial file
			outFile.Close()
			os.Remove(modelPath)
			return
		}

		// Update progress
		progress := float64(i) * 100 / float64(totalChunks)
		downloaded := int64(float64(totalSize) * progress / 100)

		mm.downloadLock.Lock()
		status := mm.downloads[modelName]
		status.Progress = progress
		status.Downloaded = downloaded
		mm.downloadLock.Unlock()
	}

	// Mark download as complete
	mm.downloadLock.Lock()

	// Update download status
	status := mm.downloads[modelName]
	status.Progress = 100
	status.Status = "completed"
	status.Completed = true
	status.Downloaded = totalSize

	// Update model status
	for i, model := range mm.models {
		if model.Name == modelName {
			mm.models[i].IsDownloaded = true
			mm.models[i].FilePath = modelPath
			break
		}
	}

	mm.downloadLock.Unlock()

	log.Printf("Download of model %s completed\n", modelName)
}

// CancelDownload cancels an in-progress download
func (mm *ModelManager) CancelDownload(modelName string) error {
	mm.downloadLock.Lock()
	defer mm.downloadLock.Unlock()

	if _, exists := mm.downloads[modelName]; !exists {
		return fmt.Errorf("no active download for model: %s", modelName)
	}

	mm.cancelDownload[modelName] = true
	return nil
}

// RemoveModel deletes a downloaded model
func (mm *ModelManager) RemoveModel(modelName string) error {
	// Check if model exists and is downloaded
	var modelToRemove *Model
	var modelIndex int
	for i, model := range mm.models {
		if model.Name == modelName {
			if !model.IsDownloaded {
				return fmt.Errorf("model is not downloaded: %s", modelName)
			}
			modelToRemove = &model
			modelIndex = i
			break
		}
	}

	if modelToRemove == nil {
		return fmt.Errorf("model not found: %s", modelName)
	}

	// Get model file path
	modelPath := filepath.Join(mm.modelsDir, modelName+".bin")
	if modelToRemove.FilePath != "" {
		modelPath = modelToRemove.FilePath
	}

	// Delete the file
	if err := os.Remove(modelPath); err != nil && !os.IsNotExist(err) {
		return fmt.Errorf("failed to delete model file: %w", err)
	}

	// Update model status
	mm.models[modelIndex].IsDownloaded = false
	mm.models[modelIndex].FilePath = ""

	// Remove from downloads if present
	mm.downloadLock.Lock()
	delete(mm.downloads, modelName)
	delete(mm.cancelDownload, modelName)
	mm.downloadLock.Unlock()

	return nil
}

// SaveModels saves the current models state to a file
func (mm *ModelManager) SaveModels(filename string) error {
	data, err := json.MarshalIndent(mm.models, "", "  ")
	if err != nil {
		return fmt.Errorf("failed to marshal models: %w", err)
	}

	if err := os.WriteFile(filename, data, 0644); err != nil {
		return fmt.Errorf("failed to write models to file: %w", err)
	}

	return nil
}

// LoadModels loads models from a file
func (mm *ModelManager) LoadModels(filename string) error {
	data, err := os.ReadFile(filename)
	if err != nil {
		if os.IsNotExist(err) {
			// File doesn't exist, just use default models
			return nil
		}
		return fmt.Errorf("failed to read models file: %w", err)
	}

	var models []Model
	if err := json.Unmarshal(data, &models); err != nil {
		return fmt.Errorf("failed to parse models file: %w", err)
	}

	mm.models = models
	mm.refreshDownloadStatus()
	return nil
}