package main

// readAll read string from clipboard
func ReadAll() (string, error) {
	return readAll()
}

// writeAll write string to clipboard
func WriteAll(text string) error {
	return writeAll(text)
}

// Unsupported might be set true during clipboard init, to help callers decide
// whether or not to offer clipboard options.
var Unsupported bool
