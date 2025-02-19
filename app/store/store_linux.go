package store

import (
	"os"
	"path/filepath"
)

func getStorePath() string {
	if os.Geteuid() == 0 {
		// TODO where should we store this on linux for system-wide operation?
		return "/etc/kc-riff/config.json"
	}

	home := os.Getenv("HOME")
	return filepath.Join(home, ".kc-riff", "config.json")
}
