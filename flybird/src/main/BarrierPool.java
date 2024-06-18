package main;

import java.util.ArrayList;
import java.util.List;

public class BarrierPool {
	private static List<Barrier> pool = new ArrayList<>();
	public static final int initCount = 6;
	public static final int maxCount = 8;
	
	static {
		for (int i = 0; i < initCount; i++) {
			pool.add(new Barrier());
		}
	}
	
	public static Barrier getPool() {
		int size = pool.size();
		if (size>0) {
			return pool.remove(size-1);
		}else {
			return new Barrier();
		}
	}
	
	public static void setPool(Barrier barrier) {
		if (pool.size()<maxCount) {
			pool.add(barrier);
		}
	}
}
