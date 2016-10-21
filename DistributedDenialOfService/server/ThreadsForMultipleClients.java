package server;

import java.io.BufferedOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.net.Socket;

public class ThreadsForMultipleClients extends Thread {

	private Socket clientSocket;

	public ThreadsForMultipleClients(Socket connection) {
		clientSocket = connection;
	}

	public void run() {
		int n;

		String isRegister="You have been registered"+" "+(char)13;
        BufferedOutputStream os;
		try {
			os = new BufferedOutputStream(clientSocket.getOutputStream());
			OutputStreamWriter osw = new OutputStreamWriter(os, "US-ASCII");
	        osw.write(isRegister);
	        osw.flush();
	        //If we close the stream the socket gets closed too
	        //os.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
}
