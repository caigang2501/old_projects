package main;

import java.awt.Font;
import java.awt.Graphics;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

import util.Constent;

public class GameBarrierLayer {
	private List<Barrier> barriers;
	private int score;
	Random random;
	GameTime gameTime;
	
	
	public GameBarrierLayer() {
		barriers = new ArrayList<>();
		random = new Random();
		gameTime = new GameTime();
	}
	
	public void draw(Graphics g,Bird bird) {
		logic(g);
		for (int i = 0; i < barriers.size(); i++) {
			if (!barriers.get(i).isOutFrame()) {
				barriers.get(i).draw(g);
			}else {
				BarrierPool.setPool(barriers.remove(i));
				i--;
			}
		}
		collideBird(bird);
	}	
	
	private void logic(Graphics g) {
		if (barriers.size()==0) {
			gameTime.begain();
			insert(Constent.FRAM_WEITH,100+random.nextInt(200),3);
		}else {
			long differ = gameTime.differ();
			g.setFont(new Font("微软雅黑",1,20));
			g.drawString("坚持了"+differ+"秒", 30, 70);
			
			score = getScore();
			if(differ<=score) {
				g.drawString("最高成绩:"+score+"秒", 200, 70);
			}else {
				setScore(String.valueOf(differ));
				g.drawString("最高成绩:"+score+"秒", 200, 70);
			}
			
			Barrier last = barriers.get(barriers.size()-1);
			if (last.isInFrame()) {
				insert(Constent.FRAM_WEITH,100+random.nextInt(200),3);
			}
		}
	}
	
	private void insert(int x,int y,int speed) {
		Barrier barrier = BarrierPool.getPool();
		barrier.setX(x);
		barrier.setY(y);
		barrier.setSpeed(speed);
		barriers.add(barrier);
	}
	
	private boolean collideBird(Bird bird) {
		for (int i = 0; i < barriers.size(); i++) {
			if (barriers.get(i).getRect().intersects(bird.getRect())||
					barriers.get(i).getRectd().intersects(bird.getRect())) {
				bird.life = false;
			}
		
		}
		return false;
	}
	
	public void restart() {
		barriers.clear();
	}
	
	
	
	File file = new File("C:\\Users\\dell\\eclipse-workspace\\flybird\\src\\main\\score.txt");
	public int getScore() {
		BufferedReader in = null;
		try {
			in = new BufferedReader(new FileReader(file));
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		int read = 0;
		try {
			read = Integer.parseInt(in.readLine());
		} catch (NumberFormatException | IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		try {
			in.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return read;
	}
	
	public void setScore(String str) {
		FileWriter fileWriter = null;
		try {
			fileWriter = new FileWriter(file);
		} catch (IOException e2) {
			// TODO Auto-generated catch block
			e2.printStackTrace();
		}
		try {
			fileWriter.write(str);
		} catch (IOException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
		try {
			fileWriter.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
}
