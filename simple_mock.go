package main

import "C"
import (
	"encoding/json"
	"fmt"
)

//export GetHealthCheck
func GetHealthCheck() *C.char {
	return C.CString(`{"status":"ok","version":"0.1.0","name":"KC-Riff"}`)
}

//export GetModels
func GetModels() *C.char {
	models := []map[string]interface{}{
		{
			"name":        "llama2",
			"description": "A foundational language model",
			"tags":        []string{"base", "popular"},
			"size":        3800000000,
			"downloaded":  false,
			"recommended": true,
			"version":     "2.0.0",
		},
		{
			"name":        "mistral",
			"description": "Instruction following model",
			"tags":        []string{"instruction"},
			"size":        4200000000,
			"downloaded":  false,
			"recommended": true,
			"version":     "0.1",
		},
	}
	
	jsonData, _ := json.Marshal(models)
	return C.CString(string(jsonData))
}

//export DownloadModel
func DownloadModel(modelName *C.char) *C.char {
	name := C.GoString(modelName)
	return C.CString(fmt.Sprintf(`{"status":"downloading","model":"%s"}`, name))
}

//export GetDownloadStatus
func GetDownloadStatus(modelName *C.char) *C.char {
	name := C.GoString(modelName)
	return C.CString(fmt.Sprintf(`{"model":"%s","progress":50.0,"completed":false}`, name))
}

//export RemoveModel
func RemoveModel(modelName *C.char) *C.char {
	name := C.GoString(modelName)
	return C.CString(fmt.Sprintf(`{"status":"removed","model":"%s"}`, name))
}

//export CheckForUpdatesC
func CheckForUpdatesC() *C.char {
	return C.CString(`{"available":false,"current_version":"0.1.0"}`)
}

//export ApplyUpdate
func ApplyUpdate() *C.char {
	return C.CString(`{"error":"No update available"}`)
}

func main() {}
