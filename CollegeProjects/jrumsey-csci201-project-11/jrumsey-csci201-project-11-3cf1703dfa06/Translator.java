import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.Scanner;

//Jeremy Rumsey
//Project 11

public class Translator {

	public static int labelNum = 0;
	public static int skipNum = 0;
	public static int returnNum = 0;
	
	public static void main(String[] args) {
		Scanner reader = new Scanner(System.in);
		System.out.println("Please enter vm file to be translated: ");
		String fileName = reader.next();
	    String currentLine;
	    try {
	        FileReader fileReader = 
	            new FileReader(fileName);
	        BufferedReader bufferedReader = 
	            new BufferedReader(fileReader);

	        while((currentLine = bufferedReader.readLine()) != null) {
	        	
	        	currentLine = currentLine.trim();		// takes away white space
	        	if(currentLine.contains("//"))			// deletes any comments
	        	{
	        		currentLine = currentLine + " ";
	        		String[] splitLine = currentLine.split("//");
	        		String splitLine1 = splitLine[0];
	        		currentLine = splitLine1;
	        	}
//	        	System.out.println("\n");
//	        	System.out.println("//" + currentLine);
	        	String[] splitLine = currentLine.split(" ");
        		String splitLine1 = splitLine[0];
	        	if(splitLine1.equals("push"))
	        	{
	        		if(currentLine.contains("constant"))
	        		{
	        			String number = currentLine.substring(14, currentLine.length());
	        			System.out.println("@" + number + " D=A @SP A=M M=D @SP M=M+1".replaceAll("\\s+","\n"));
	        			
	           		}
	        		else if(currentLine.contains("static"))
	        		{
	        			String number = currentLine.substring(12, currentLine.length());
	        			System.out.println("@" + number + " D=A @SP A=M M=D @SP M=M+1".replaceAll("\\s+","\n"));
	        		}
	           		else if(currentLine.contains("local"))
	        		{
	           			String number = currentLine.substring(11, currentLine.length());
	        			System.out.println("@" + number + " D=A @LCL A=M D=D+A A=D D=M @SP A=M M=D @SP M=M+1".replaceAll("\\s+","\n"));
	        		}
	           		else if(currentLine.contains("argument"))
	        		{
	           			String number = currentLine.substring(14, currentLine.length());
	        			System.out.println("@" + number + " D=A @ARG A=M D=D+A A=D D=M @SP A=M M=D @SP M=M+1".replaceAll("\\s+","\n"));
	        		}
	           		else if(currentLine.contains("temp"))
	        		{
	           			String number = currentLine.substring(10, currentLine.length());
	           			int numberInt = Integer.parseInt(number) + 5;
	        			System.out.println("@" + Integer.toString(numberInt) + " D=M @SP A=M M=D @SP M=M+1".replaceAll("\\s+","\n"));
	        		}
	        	}
	        	
	        	if(splitLine1.equals("pop"))
	        	{
	        		if(currentLine.contains("local"))
	        		{
	        			String number = currentLine.substring(10, currentLine.length());
	        			String command = "@" + number + " D=A @LCL A=M D=D+A @LCL M=D @SP M=M-1 A=M D=M @LCL A=M M=D @" + number 
	        					+ " D=A @LCL A=M D=A-D @LCL M=D";
	        			System.out.println(command.replaceAll("\\s+","\n"));
	        		}
	        		if(currentLine.contains("argument"))
	        		{
	        			String number = currentLine.substring(13, currentLine.length());
	        			String command = "@" + number + " D=A @ARG A=M D=D+A @ARG M=D @SP M=M-1 A=M D=M @ARG A=M M=D @" + number 
	        					+ " D=A @ARG A=M D=A-D @ARG M=D";
	        			System.out.println(command.replaceAll("\\s+","\n"));
	        		}
	        		if(currentLine.contains("temp"))
	        		{
	        			String number = currentLine.substring(9, currentLine.length());
	        			int numberInt = Integer.parseInt(number) + 5;
	        			String command = "@SP M=M-1 A=M D=M @" + Integer.toString(numberInt) +  " M=D";
	        			System.out.println(command.replaceAll("\\s+","\n"));
	        		}
	        		
	        	}
	        	
	        	if(splitLine1.equals("add"))
	        	{
	        		System.out.println("@SP A=M-1 D=M @SP M=M-1 @SP A=M-1 M=M+D".replaceAll("\\s+","\n"));
	        	}
	        	
	        	if(splitLine1.equals("sub"))
	        	{
	        		System.out.println("@SP A=M-1 D=M @SP M=M-1 @SP A=M-1 M=M-D".replaceAll("\\s+","\n"));
	        	}
	        	
	        	if(splitLine1.equals("eq"))
	        	{
	        		String command = "@SP M=M-1 A=M D=M M=0 A=A-1 D=D-M @Label" + labelNum+ " D;JEQ @SP A=M-1 M=0 @Skip" + skipNum + " 0;JMP "
	        				+ "(Label" + labelNum + ") @SP A=M-1 M=-1 (Skip" + skipNum + ")";
	        		System.out.println(command.replaceAll("\\s+","\n"));
	        		labelNum++;
	        		skipNum++;
	        	}
	        	if(splitLine1.equals("gt"))
	        	{
	        		String command = "@SP M=M-1 A=M D=M M=0 A=A-1 D=D-M @Label" + labelNum+ " D;JLT @SP A=M-1 M=0 @Skip" + skipNum + " 0;JMP "
	        				+ "(Label" + labelNum + ") @SP A=M-1 M=-1 (Skip" + skipNum + ")";
	        		System.out.println(command.replaceAll("\\s+","\n"));
	        		labelNum++;
	        		skipNum++;
	        	}
	        	if(splitLine1.equals("lt"))
	        	{
	        		String command = "@SP M=M-1 A=M D=M M=0 A=A-1 D=D-M @Label" + labelNum+ " D;JGT @SP A=M-1 M=0 @Skip" + skipNum + " 0;JMP "
	        				+ "(Label" + labelNum + ") @SP A=M-1 M=-1 (Skip" + skipNum + ")";
	        		System.out.println(command.replaceAll("\\s+","\n"));
	        		labelNum++;
	        		skipNum++;
	        	}
	        	if(splitLine1.equals("neg"))
	        	{
	        		System.out.println("@SP A=M-1 M=-M".replaceAll("\\s+","\n"));
	        	}
	        	if(splitLine1.equals("and"))
	        	{
	        		System.out.println("@SP M=M-1 A=M D=M M=0 @SP A=M-1 D=D&M @SP M=M-1 A=M M=D @SP M=M+1".replaceAll("\\s+","\n"));
	        	}
	        	if(splitLine1.equals("or"))
	        	{
	        		System.out.println("@SP M=M-1 A=M D=M M=0 @SP A=M-1 D=D|M @SP M=M-1 A=M M=D @SP M=M+1".replaceAll("\\s+","\n"));
	        	}
	        	if(splitLine1.equals("not"))
	        	{
	        		System.out.println("@SP A=M-1 M=!M".replaceAll("\\s+","\n"));
	        	}
	        	if(currentLine.contains("goto"))
	        	{
	        		if(currentLine.contains("if-goto"))
		        	{
		        		String command = "@SP M=M-1 A=M D=M @" + currentLine.substring(8, currentLine.length()) + " D;JNE";
		        		System.out.println(command.replaceAll("\\s+","\n"));
		        	}
	        		else{
	        		String command = "@" + currentLine.substring(5, currentLine.length()) + " 0;JMP";
	        		System.out.println(command.replaceAll("\\s+","\n"));
		        	}
	        	}
	        	
	        	if(splitLine1.equals("label"))
	        	{
	        		String command = "(" + currentLine.substring(6, currentLine.length()) + ")";
	        		System.out.println(command.replaceAll("\\s+","\n"));
	        	}
	        	
	        	if(splitLine1.equals("function"))
	        	{
	        		
	        		String command = "(" + splitLine[1] + ") @SP A=M M=0 A=A+1 M=0 @" + splitLine[2] + " D=A @SP M=D+M";
	        		System.out.println(command.replaceAll("\\s+","\n"));
	        	}
	        	if(splitLine1.equals("call"))
	        	{
	        		String command = "@return" + returnNum + " D=A @SP A=M M=D @SP M=M+1 @LCL D=M @SP A=M M=D @SP M=M+1 @ARG D=M "
	        				+ "@SP A=M M=D @SP M=M+1 @THIS D=M @SP A=M M=D @SP M=M+1 @THAT D=M @SP A=M M=D  @SP M=M+1 D=M "
	        				+ "@" + splitLine[2] + " D=D-A @5 D=D-A @ARG M=D @SP D=M @LCL M=D @" + splitLine[1] + " 0;JMP (return" + returnNum + ")";
	        		System.out.println(command.replaceAll("\\s+","\n"));
	        		returnNum++;
	        	}
	        	if(splitLine1.equals("return"))
	        	{
	        		String command = "@LCL D=M @R14 M=D @5 A=D-A D=M @R13 M=D @SP M=M-1 A=M D=M @ARG A=M M=D @ARG D=M+1 @SP M=D @R14 M=M-1 A=M D=M @THAT "
	        				+ "M=D @R14 M=M-1 A=M D=M @THIS M=D @R14 M=M-1 A=M D=M @ARG M=D @R14 M=M-1 A=M D=M @LCL M=D @R13 A=M 0;JMP";
	        		System.out.println(command.replaceAll("\\s+","\n"));
	        	}
	        }
	        bufferedReader.close();         
	    }
	    catch(FileNotFoundException ex) {
	        System.out.println(
	            "Unable to open file '" + 
	            fileName + "'");                
	    }
	    catch(IOException ex) {
	        System.out.println(
	            "Error reading file '" 
	            + fileName + "'");                  
	    }

	}

}
