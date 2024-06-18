package util;

import java.awt.image.BufferedImage;
import java.awt.image.ImageProducer;
import java.io.FileInputStream;
import java.io.IOException;

import javax.imageio.ImageIO;

public class GameUtil {
	public static BufferedImage loadBufferedImage(String ImgPath) {
		try {
			return ImageIO.read(new FileInputStream(ImgPath));
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return null;
	}
	
	
	
}