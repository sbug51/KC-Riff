//go:build windows
// +build windows

package readline

import (
	"errors"

	"golang.org/x/sys/windows"
)

// Termios represents terminal settings for Windows.
// This is a minimal implementation using console mode flags.
type Termios struct {
	mode uint32
}

// getTermios retrieves the console mode for the given file descriptor.
func getTermios(fd uintptr) (*Termios, error) {
	// Convert fd to a Windows handle.
	handle := windows.Handle(fd)
	var mode uint32
	err := windows.GetConsoleMode(handle, &mode)
	if err != nil {
		return nil, err
	}
	return &Termios{mode: mode}, nil
}

// setTermios sets the console mode for the given file descriptor.
func setTermios(fd uintptr, termios *Termios) error {
	if termios == nil {
		return errors.New("termios is nil")
	}
	handle := windows.Handle(fd)
	return windows.SetConsoleMode(handle, termios.mode)
}
