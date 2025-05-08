package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"sync"
	"time"
)

// Simple model structure
type Model struct {
	Name          string   `json:"name"`
	Description   string   `json:"description"`
	Size          int64    `json:"size"`
	Parameters    int64    `json:"parameters"`
	Tags          []string `json:"tags"`
	Category      string   `json:"category"`
	IsDownloaded  bool     `json:"downloaded"`
	KCRecommended bool     `json:"kc_recommended"`
}

// Download status structure
type DownloadStatus struct {
	ModelName  string  `json:"model_name"`
	Progress   float64 `json:"progress"`
	Status     string  `json:"status"`
	Error      string  `json:"error,omitempty"`
	Completed  bool    `json:"completed"`
	Downloaded int64   `json:"downloaded_bytes"`
	TotalSize  int64   `json:"total_bytes"`
}

var (
	models = []Model{
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
	}

	downloadMutex sync.Mutex
	downloads     = make(map[string]*DownloadStatus)
)

func main() {
	port := getPort()
	fmt.Printf("Starting minimal server on http://0.0.0.0:%s\n", port)

	http.HandleFunc("/api/models", getModelsHandler)
	http.HandleFunc("/api/models/download", downloadModelHandler)
	http.HandleFunc("/api/models/status", getDownloadStatusHandler)
	http.HandleFunc("/api/models/remove", removeModelHandler)
	http.HandleFunc("/api/health", healthCheckHandler)
	http.HandleFunc("/api/updates", checkUpdatesHandler)
	http.HandleFunc("/api/updates/apply", applyUpdateHandler)

	http.ListenAndServe(":"+port, nil)
}

func getPort() string {
	// Default to port 5000
	port := "5000"
	if envPort := os.Getenv("PORT"); envPort != "" {
		port = envPort
	}
	return port
}

func getModelsHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(models)
}

func downloadModelHandler(w http.ResponseWriter, r *http.Request) {
	modelName := r.URL.Query().Get("name")
	if modelName == "" {
		http.Error(w, "Model name is required", http.StatusBadRequest)
		return
	}

	// Check if model exists
	var modelExists bool
	for _, model := range models {
		if model.Name == modelName {
			modelExists = true
			break
		}
	}

	if !modelExists {
		http.Error(w, "Model not found", http.StatusNotFound)
		return
	}

	// Check if already downloading
	downloadMutex.Lock()
	status, exists := downloads[modelName]
	if !exists {
		// Create new download
		status = &DownloadStatus{
			ModelName:  modelName,
			Progress:   0,
			Status:     "downloading",
			Completed:  false,
			Downloaded: 0,
			TotalSize:  0,
		}
		downloads[modelName] = status

		// Start download in background
		go simulateDownload(modelName)
	}
	downloadMutex.Unlock()

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(status)
}

func getDownloadStatusHandler(w http.ResponseWriter, r *http.Request) {
	modelName := r.URL.Query().Get("name")
	if modelName == "" {
		http.Error(w, "Model name is required", http.StatusBadRequest)
		return
	}

	// Check if model is already downloaded
	for i, model := range models {
		if model.Name == modelName && model.IsDownloaded {
			status := &DownloadStatus{
				ModelName:  modelName,
				Progress:   100,
				Status:     "completed",
				Completed:  true,
				Downloaded: model.Size,
				TotalSize:  model.Size,
			}
			w.Header().Set("Content-Type", "application/json")
			json.NewEncoder(w).Encode(status)
			return
		}
	}

	// Check if currently downloading
	downloadMutex.Lock()
	status, exists := downloads[modelName]
	downloadMutex.Unlock()

	if !exists {
		// Not downloaded and not in progress
		status = &DownloadStatus{
			ModelName: modelName,
			Progress:  0,
			Status:    "not_started",
			Completed: false,
		}
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(status)
}

func removeModelHandler(w http.ResponseWriter, r *http.Request) {
	modelName := r.URL.Query().Get("name")
	if modelName == "" {
		http.Error(w, "Model name is required", http.StatusBadRequest)
		return
	}

	// Find the model and update its status
	var modelFound bool
	for i, model := range models {
		if model.Name == modelName {
			modelFound = true
			if !model.IsDownloaded {
				http.Error(w, "Model is not downloaded", http.StatusBadRequest)
				return
			}
			models[i].IsDownloaded = false
			break
		}
	}

	if !modelFound {
		http.Error(w, "Model not found", http.StatusNotFound)
		return
	}

	// Remove from downloads
	downloadMutex.Lock()
	delete(downloads, modelName)
	downloadMutex.Unlock()

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]interface{}{
		"status":  "success",
		"message": "Model removed successfully",
	})
}

func healthCheckHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]interface{}{
		"status":  "healthy",
		"version": "0.1.0",
	})
}

func checkUpdatesHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]interface{}{
		"available":       true,
		"current_version": "0.1.0",
		"new_version":     "0.2.0",
		"release_date":    time.Now().Format(time.RFC3339),
		"release_notes":   "Bug fixes and performance improvements",
	})
}

func applyUpdateHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]interface{}{
		"status":  "success",
		"message": "Update applied successfully",
	})
}

func simulateDownload(modelName string) {
	// Get model size
	var modelSize int64
	for _, model := range models {
		if model.Name == modelName {
			modelSize = model.Size
			break
		}
	}

	// Update status
	downloadMutex.Lock()
	status := downloads[modelName]
	status.TotalSize = modelSize
	downloadMutex.Unlock()

	// Simulate download progress
	totalChunks := 20
	for i := 1; i <= totalChunks; i++ {
		// Check if we should cancel
		downloadMutex.Lock()
		if status, exists := downloads[modelName]; exists && status.Status == "cancelled" {
			downloadMutex.Unlock()
			return
		}
		
		// Update progress
		progress := float64(i) * 100 / float64(totalChunks)
		downloaded := int64(float64(modelSize) * progress / 100)
		
		status := downloads[modelName]
		status.Progress = progress
		status.Downloaded = downloaded
		downloadMutex.Unlock()

		// Sleep to simulate network delay
		time.Sleep(500 * time.Millisecond)
	}

	// Mark as completed
	downloadMutex.Lock()
	status = downloads[modelName]
	status.Progress = 100
	status.Status = "completed"
	status.Completed = true
	status.Downloaded = modelSize

	// Update model
	for i, model := range models {
		if model.Name == modelName {
			models[i].IsDownloaded = true
			break
		}
	}
	downloadMutex.Unlock()

	// Log completion
	log.Printf("Download of model %s completed\n", modelName)
}