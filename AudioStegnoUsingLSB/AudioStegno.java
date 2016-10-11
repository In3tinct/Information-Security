package stegno;

import java.io.BufferedInputStream;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;

public class AudioStegno {
	
	static WavFile outwavFile =null;
	
	static long frameCounter = 0;
	public static void main(String args[]){
		
		//Size of the original file is 661544 bytes, this buffer contains the updated bytes
		byte[] buffer1 = new byte[661544];  
		
		try
	      {
	    	  
	    	  int sampleRate = 44100;		// Samples per second

				// Calculate the number of frames required for specified duration
			  long numFrames = 165375;
			  int count=0;

				// Create a wav file with the name specified as the first argument
			 outwavFile = WavFile.newWavFile(new File("C:\\Users\\Vaibhav\\Desktop\\cello2.wav"), 2, numFrames, 16, sampleRate);
				
	         
	         /////////////////////////////////////////////////////////////////////////////////////
	         ByteArrayOutputStream out = new ByteArrayOutputStream();
	         BufferedInputStream in = new BufferedInputStream(new FileInputStream("C:\\Users\\Vaibhav\\Desktop\\cello1.wav"));

	         int read;
	         byte[] buff = new byte[1024];
	         while ((read = in.read(buff)) > 0)
	         {
	             out.write(buff, 0, read);
	         }
	         out.flush();
	         byte[] audioBytes = out.toByteArray();
	         
	        
	         	//Text to hide 'Hi' in binary
	        	String texttohide="0100100001101001";
	        	char [] texttohidechar= texttohide.toCharArray();
	         
	         //Starting from 44 because the first 43 bytes is the header of the file
	         for(int i=44; i<audioBytes.length;i++){	
	        	
	        	//http://stackoverflow.com/questions/9609394/java-byte-array-contains-negative-numbers
	        	//removing the negative values we were getting for the bytes
	        	Integer a=audioBytes[i] & 0xff;
	        	
	        	//Converting the bytes to binary
	        	String bytestobinary = String.format("%8s", Integer.toBinaryString(a & 0xFF)).replace(' ', '0');
	        
	        	
	        	// texttohidechar[count] this will character one by one
	        	
	        	//byte's only allow numbers in the range of -128 to 127. 
	        	//I would use an int instead, which holds numbers in the range of -2.1 billion to 2.1 billion.
	        	//And later using Byte.parseByte was giving error for 255
	        	
	        	//Since our message will take only 16 bits, so we will only input 16 bits, once it is 
	        	//done we simple copy rest of the stream.
	        	
	        	if(a<127 && count<16){
	        	String manupulatedBinary=bytestobinary.substring(0,7)+texttohidechar[count];
	        	count++;
	        	/*System.out.println("Original"+bytestobinary);
	        	System.out.println(manupulatedBinary);*/
	        	
	        	byte b = Byte.parseByte(manupulatedBinary, 2);
	        	
	        	
	        	buffer1[i]=b;
	        	/*System.out.println("Last i"+i);*/
	        	}else{
	        		//This Copy rest of the bytes
	        		//System.out.println(a);
	        		
		        	buffer1[i]=a.byteValue();
	        	}
	        	    
	         }
	         
	         outwavFile.close();
	         System.out.println("Bytes read and new byte stream generated");
	         WriteUpdatedBytes w=new WriteUpdatedBytes();
	         w.main(buffer1);
	         fetchHiddenMessageFromNewFile();
	         
	         
	      }
	      catch (Exception e)
	      {
	         System.err.println(e);
	      }
	   }
	
	
	public static void fetchHiddenMessageFromNewFile() throws IOException{
		String secretmessage="";
		try {
			ByteArrayOutputStream out = new ByteArrayOutputStream();
	        BufferedInputStream in;
			in = new BufferedInputStream(new FileInputStream("C:\\Users\\Vaibhav\\Desktop\\cellowithhiddenmessage.wav"));
		

        int read;
        byte[] buff = new byte[1024];
        while ((read = in.read(buff)) > 0)
        {
            out.write(buff, 0, read);
        }
        out.flush();
        byte[] audioBytes = out.toByteArray();
        
        
        for(int i=88;i<230;i++){
			  
		  	Integer a=audioBytes[i] & 0xff;
        	
        	//Converting the bytes to binary
        	String bytestobinary = String.format("%8s", Integer.toBinaryString(a & 0xFF)).replace(' ', '0');
		    
				  if(a<127){
					  char secretMessage=bytestobinary.charAt(7);
					  secretmessage+=String.valueOf(secretMessage);
					  
				  }
	  }
        		
        System.out.println("Hidden message in bits:"+secretmessage);
        		
        String input = secretmessage;
        String output = "";
        for(int i = 0; i <= input.length() - 8; i+=8)
        {
            int k = Integer.parseInt(input.substring(i, i+8), 2);
            output += (char) k;
        }   
        System.out.println("Hidden message retrieved is:"+output);
        
        
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
	}
}
