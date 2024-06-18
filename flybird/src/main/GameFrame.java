package main;

import java.awt.Frame;
import java.awt.Graphics;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.awt.event.WindowListener;
import java.awt.image.BufferedImage;

import javax.swing.WindowConstants;

import util.Constent;
import util.GameUtil;

public class GameFrame extends Frame {
	GameBackGraund gameBackGraund;
	
	private Bird bird;
	
	GameFrontGround gameFrontGround;
	
	private GameBarrierLayer gameBarrierLayer;
	
	private BufferedImage buffimg = new BufferedImage(Constent.FRAM_WEITH, Constent.FRAM_HIGH,BufferedImage.TYPE_4BYTE_ABGR);
	
	public GameFrame() {
		setVisible(true);
		setSize(Constent.FRAM_WEITH, Constent.FRAM_HIGH);
		setTitle(Constent.FRAM_TETLE);
		setLocation(Constent.FRAM_X, Constent.FRAM_Y);
		setResizable(false);
		
		addWindowListener(new WindowAdapter() {

			@Override
			public void windowClosing(WindowEvent e) {
				// TODO Auto-generated method stub
				System.exit(0);
			}
			
		});
		
		initGame();
		new run().start();
		
		addKeyListener(new KeyAdapter() {

			@Override
			public void keyPressed(KeyEvent e) {
				add(e);
			}

			@Override
			public void keyReleased(KeyEvent e) {
				minu(e);
			}
			
		});
		
	}
	
	public void initGame() {
		gameBackGraund = new GameBackGraund();
		bird = new Bird();
		gameFrontGround = new GameFrontGround();
		gameBarrierLayer = new GameBarrierLayer();
	
	}
	
	class run extends Thread{
		@Override
		public void run() {
			while (true) {
				repaint();
				try {
					Thread.sleep(30);
				} catch (InterruptedException e) {
					e.printStackTrace();
				}
			}
		}
				
	}
	
	@Override
	public void update(Graphics g) {
		if (bird.life) {
			Graphics graphics = buffimg.getGraphics();
			
			gameBackGraund.draw(graphics);
			bird.draw(graphics);
			gameFrontGround.draw(graphics);
			gameBarrierLayer.draw(graphics,bird);
			g.drawImage(buffimg, 0, 0, null);
		}else {
			BufferedImage imgGameOver = GameUtil.loadBufferedImage("img/gameover.png");
			g.drawImage(imgGameOver, 170, 0, null);
		}
		
		
	}
	
	public void add(KeyEvent e) {
		switch (e.getKeyCode()) {
			case KeyEvent.VK_UP:
				bird.fly(1);
				break;
			case KeyEvent.VK_SPACE:
				restart();
				break;

		}
	}
	

	public void minu(KeyEvent e) {
		switch (e.getKeyCode()) {
			case KeyEvent.VK_UP:
				bird.fly(5);
				break;

		}
	}
	private void restart() {
		gameBarrierLayer.restart();
		bird.restart();
	}
}
