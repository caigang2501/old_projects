package main;

import java.awt.Graphics;
import java.awt.image.BufferedImage;

public class Cloud {
	private BufferedImage img;
	private int speed;
	private int x,y;
	
	public Cloud() {}

	public Cloud(BufferedImage img, int speed, int x, int y) {
		super();
		this.img = img;
		this.speed = speed;
		this.x = x;
		this.y = y;
	}
	
	public void draw(Graphics g) {
		x -= speed;
		g.drawImage(img, x, y, null);
	}
	
	public boolean isOutFrame() {
		return x<-100;
	}
}
