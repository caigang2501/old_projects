package main;

import java.awt.Graphics;
import java.awt.Rectangle;
import java.awt.image.BufferedImage;

import util.Constent;
import util.GameUtil;

public class Bird {
	private BufferedImage[] images;
	public static final int BIRD_IMG_COUNT = 3;
	
	private int state;
	public static final int STATE_NOMAL = 0;
	public static final int STATE_UP = 1;
	public static final int STATE_DOWN = 2;
	
	
	private int x=200,y=200;
	private boolean up = false,down=false;
	private float speed=0;
	private float accelerate = (float) 0.2;
	public boolean life = true;
	
	

	private Rectangle rect;
	
	
	public Bird() {
		images = new BufferedImage[BIRD_IMG_COUNT];
		for(int i=0;i<BIRD_IMG_COUNT;i++) {
			images[i] = GameUtil.loadBufferedImage(Constent.BIRD_IMG[i]);
		}
		
		int w = images[0].getWidth()-6;
		int h = images[0].getHeight()-6;
		rect = new Rectangle(w,h);
	}
	
	
	public void draw(Graphics g) {
		flyLogic();
		g.drawImage(images[state], x, y,null);
//		g.drawRect(x+6, y+8, rect.width-7, rect.height-7);
		rect.x = this.x+6;
		rect.y = this.y+8;
	}
	
	public void flyLogic() {
		System.out.println(speed);
		if (up) {
			speed = -3;
			y+=speed;
			if (y<30) {
				y=30;
				speed = 0;
			}
		}
		if (!up) {
			speed += accelerate;
			y+=speed;
			if (y>Constent.FRAM_HIGH-50) {
				y=Constent.FRAM_HIGH-50;
				speed = 0;
			}
		}
	}
	
	public void fly(int fly) {
		switch(fly) {
			case 1:
				state = 1;
				up=true;
				break;
			case 5:
				state = 2;
				up=false;
				break;
					
		}
			
	}
	public void restart() {
		life = true;
		x = 200;
		y = 200;
	}
	
	public Rectangle getRect() {
		return rect;
	}


	public void setRect(Rectangle rect) {
		this.rect = rect;
	}
}
