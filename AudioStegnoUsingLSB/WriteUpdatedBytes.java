package stegno;

import java.io.ByteArrayInputStream;
import java.io.File;

import javax.sound.sampled.AudioFileFormat;
import javax.sound.sampled.AudioFormat;
import javax.sound.sampled.AudioInputStream;
import javax.sound.sampled.AudioSystem;

public class WriteUpdatedBytes
{
	public void main(byte [] res)
	{
		
		  byte[] pcm_data = res;
		 
		  AudioFormat frmt = new AudioFormat(44100, 16, 2, false, false);
		  AudioInputStream ais = new AudioInputStream(
		    new ByteArrayInputStream(pcm_data), frmt, 
		    pcm_data.length / frmt.getFrameSize()
		  );
		 
		  try {
		    AudioSystem.write(ais, AudioFileFormat.Type.WAVE, new
		      File("C:\\Users\\Vaibhav\\Desktop\\cellowithhiddenmessage.wav")
		    );
		    System.out.println("New wav file with hidden information generated");
		  } 
		  catch(Exception e) {
		    e.printStackTrace();
		  }
		  
		  
		}
		
	}

