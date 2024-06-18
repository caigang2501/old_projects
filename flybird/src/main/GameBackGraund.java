package main;

import java.awt.Color;
import java.awt.Graphics;
import java.awt.image.BufferedImage;

import util.Constent;
import util.GameUtil;

public class GameBackGraund {
	private BufferedImage bkimge;
	
	public GameBackGraund() {
		bkimge = GameUtil.loadBufferedImage(Constent.BK_IMG_PATH);
	}
	
	public void draw(Graphics g) {
		
		g.setColor(Constent.BK_COLOR);
		g.fillRect(0, 0, Constent.FRAM_WEITH, Constent.FRAM_HIGH);
		g.setColor(Color.black);
		
		int height = bkimge.getHeight();
		int weight = bkimge.getWidth();
		int count = Constent.FRAM_WEITH/weight+1;
		for(int i=0;i<count;i++) {
			g.drawImage(bkimge, weight*i, Constent.FRAM_HIGH-height,null);
		}
	}
}
