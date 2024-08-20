// Utility function for creating 2D vectors
function vec2(x, y) {
	return { x, y };
}

function ballCollisionWithTheEdges(game) {
	if (game.ball.pos.y + game.ball.radius > game.height || game.ball.pos.y - game.ball.radius <= 0) {
		game.ball.velocity.y *= -1;
	}

	if (game.ball.pos.x + game.ball.radius > game.width || game.ball.pos.x - game.ball.radius <= 0) {
		game.ball.velocity.x *= -1;
	}
}

function paddleCollisionWithTheEdges(game) {
	if (game.paddle1.pos.y <= 0)
		game.paddle1.pos.y = 0;

	if (game.paddle1.pos.y + game.paddle1.height >= game.height)
			game.paddle1.pos.y = game.height - game.paddle1.height;
}
