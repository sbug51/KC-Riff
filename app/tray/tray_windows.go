package tray

import (
	"github.com/sbug51/kcriff/app/tray/wintray"
)

func InitPlatformTray(icon, updateIcon []byte) (commontray.kcriffTray, error) {
	return wintray.InitTray(icon, updateIcon)
}
