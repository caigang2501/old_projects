package main;

public class GameTime {
	private long beginTime;
	private long endTime;
	private long differ;
	
	public GameTime() {
		
	}
	
	public void begain() {
		beginTime = System.currentTimeMillis();
	}
	
	public long differ() {
		differ = (System.currentTimeMillis()-beginTime)/1000;
		return differ;
	}
}
