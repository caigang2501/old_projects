package main;

import java.awt.Graphics;
import java.awt.Rectangle;
import java.awt.image.BufferedImage;

import util.Constent;
import util.GameUtil;

public class Barrier {
	private static BufferedImage[] imgs;
	private Rectangle rect,rectd;
	
	static {
		final int COUNT = 3;
		imgs = new BufferedImage[COUNT];
		for (int i = 0; i < COUNT; i++) {
			imgs[i] = GameUtil.loadBufferedImage(Constent.BARRIER_IMG[i]);
		}
	}
	
	private int x,y;
	private int width,height;
	private int type;
	private int speed;
	
	public static final int TYPE_NORMAL = 0;
	public static final int TYPE_UP = 1;
	public static final int TYPE_DOWN = 2;
	
	public static final int BARRIER_WIDHT = imgs[0].getWidth();
	public static final int BARRIER_NORMAL_HEIGHT = imgs[0].getHeight();
	public static final int BARRIER_UP_HEIGHT = imgs[1].getHeight();
	public static final int BARRIER_DOWN_HEIGHT = imgs[2].getHeight();
	
	public Barrier() {
		rect = new Rectangle();
		rectd = new Rectangle();
	}

	
	public void draw(Graphics g) {
		x -= speed;
		drawBarrier(g);
	}
	
	private void drawBarrier(Graphics g) {
		int count = y/BARRIER_NORMAL_HEIGHT+1;
		
		for (int i = 0; i < count; i++) {
			g.drawImage(imgs[0], x, y-i*BARRIER_NORMAL_HEIGHT, null);
		}
		g.drawImage(imgs[1], x, y, null);
//		g.drawRect(x, 0, imgs[1].getWidth(), y+imgs[1].getHeight()-15);
		setRectangle(x, 0, imgs[1].getWidth(), y+imgs[1].getHeight()-15);
		
		int countdown = (400-y)/BARRIER_NORMAL_HEIGHT+1;
		for (int i = 0; i < countdown; i++) {
			g.drawImage(imgs[0], x, 220+y+i*BARRIER_NORMAL_HEIGHT, null);
		}
		g.drawImage(imgs[2], x, 220+y-BARRIER_DOWN_HEIGHT, null);
//		g.drawRect(x, 240+y-BARRIER_DOWN_HEIGHT, imgs[2].getWidth(), Constent.FRAM_HIGH-y-120);
		setRectangled(x, 240+y-BARRIER_DOWN_HEIGHT, imgs[2].getWidth(), Constent.FRAM_HIGH-y-120);
	}
	
	public Rectangle getRectd() {
		return rectd;
	}


	public void setRectd(Rectangle rectd) {
		this.rectd = rectd;
	}


	public void setRectangle(int x,int y,int width,int height) {
		rect.x = x;
		rect.y = y;
		rect.width = width;
		rect.height = height;
		
	}
	public void setRectangled(int x,int y,int width,int height) {
		rectd.x = x;
		rectd.y = y;
		rectd.width = width;
		rectd.height = height;
		
	}
	
	
	public Rectangle getRect() {
		return rect;
	}


	public void setRect(Rectangle rect) {
		this.rect = rect;
	}


	public boolean isInFrame() {
		return x<Constent.FRAM_WEITH-200;
	}
	
	public boolean isOutFrame() {
		return x<-100;
	}

	public int getSpeed() {
		return speed;
	}

	public void setSpeed(int speed) {
		this.speed = speed;
	}

	public int getX() {
		return x;
	}

	public void setX(int x) {
		this.x = x;
	}

	public int getY() {
		return y;
	}

	public void setY(int y) {
		this.y = y;
	}
	
}
