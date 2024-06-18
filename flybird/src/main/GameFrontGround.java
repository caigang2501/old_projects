package main;

import java.awt.Graphics;
import java.awt.image.BufferedImage;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

import util.Constent;
import util.GameUtil;

public class GameFrontGround {
	
	private static final int CLOUD_SPEED = 1;
	private BufferedImage img;
	
	private List<Cloud> clouds;
	Random random;
	
	public GameFrontGround() {
		clouds = new ArrayList<>();
		img = GameUtil.loadBufferedImage(Constent.CLOUD_IMG);
		random = new Random();
	}
	
	public void draw(Graphics g) {
		logic();
		for (int i = 0; i < clouds.size(); i++) {
			if (!clouds.get(i).isOutFrame()) {
				clouds.get(i).draw(g);				
			}else {
				clouds.remove(i);
			}
		}
	}
	
	private void logic() {
		if (500*Math.random()<5) {
			Cloud cloud = new Cloud(img,CLOUD_SPEED,Constent.FRAM_WEITH,random.nextInt(150));
			clouds.add(cloud);
		}
	}
		
}
