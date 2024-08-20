class Paddle {
	constructor(pos, velocity, width, height) {
		this.pos = pos;
		this.velocity = velocity;
		this.width = width;
		this.height = height;
	}

	update(keysPressed) {
		if (keysPressed[UP_ARROW]){
			this.pos.y -= this.velocity.y;
		}
		if (keysPressed[DOWN_ARROW]){
			this.pos.y += this.velocity.y;
		}
	}

	draw(context) {
		context.fillStyle = "#33ff00";
		context.fillRect(this.pos.x, this.pos.y, this.width, this.height);
	}

	getHalfWidth(){
		return (this.width / 2);
	}

	getHalfHeight(){
		return (this.height / 2);
	}

	getCenter(){
		return vec2(
			this.pos.x + this.getHalfWidth(),
			this.pos.y + this.getHalfHeight()
		);
	}
}
