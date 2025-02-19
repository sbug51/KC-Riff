//go:build !windows

package tray

import (
	"errors"

	"github.com/sbug51/kc-riff/app/tray/commontray"
)

func InitPlatformTray(icon, updateIcon []byte) (commontray.kc-riffTray, error) {
	return nil, errors.New("not implemented")
}
