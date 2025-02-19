//go:build !windows

package tray

import (
	"errors"
)

func InitPlatformTray(icon, updateIcon []byte) (commontray.kcriffTray, error) {
	return nil, errors.New("not implemented")
}
