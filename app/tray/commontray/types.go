package commontray

var (
	Title   = "kc-riff"
	ToolTip = "kc-riff"

	UpdateIconName = "tray_upgrade"
	IconName       = "tray"
)

type Callbacks struct {
	Quit       chan struct{}
	Update     chan struct{}
	DoFirstUse chan struct{}
	ShowLogs   chan struct{}
}

type OllamaTray interface {
	GetCallbacks() Callbacks
	Run()
	UpdateAvailable(ver string) error
	DisplayFirstUseNotification() error
	Quit()
}
