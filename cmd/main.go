package main

import (
	"net/http"
	"os"
	"simple-restapi/internal/config"

	"github.com/gin-gonic/gin"
	"golang.org/x/exp/slog"
)

const (
	envLocal = "local"
	endDev   = "dev"
	envProd  = "prod"
)

var (
	log *slog.Logger
)

func setupLogger(env string) *slog.Logger {
	var _log *slog.Logger

	switch env {
	case envLocal:
		_log = slog.New(slog.NewTextHandler(os.Stdout, &slog.HandlerOptions{Level: slog.LevelDebug}))
	}

	return _log
}

func respond(c *gin.Context) {
	c.IndentedJSON(http.StatusOK, [3]int{1, 2, 3})
	log.Debug("respond method")
}

func main() {
	cfg := config.MustLoad()
	log = setupLogger(cfg.Env)

	router := gin.Default()
	log = log.With(slog.String("env", cfg.Env)) // чтобы в логи писать окружение local, prod и тд

	router.GET("/log", respond)
	log.Debug("Debug msg")
	router.Run(cfg.Address)
}
