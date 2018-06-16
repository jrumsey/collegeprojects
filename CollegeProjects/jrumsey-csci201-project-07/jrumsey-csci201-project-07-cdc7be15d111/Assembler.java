import java.io.*;
import java.util.*;

public class Assembler {
	public static String binaryLineA;
	public static String binaryLineC;
	public static String currentLine;
	public static String nextLine;
	public static String firstHalf;
	public static String secondHalf;
	
	public static void main(String[] args){

	HashMap<String, String> hashMapA0 = new HashMap<String, String>();
	hashMapA0.put("0", "101010");
	hashMapA0.put("1", "111111");
	hashMapA0.put("-1", "111010");
	hashMapA0.put("D", "001100");
	hashMapA0.put("A", "110000");
	hashMapA0.put("!D", "001101");
	hashMapA0.put("!A", "110001");
	hashMapA0.put("-D", "001111");
	hashMapA0.put("-A", "110011");
	hashMapA0.put("D+1", "011111");
	hashMapA0.put("A+1", "110111");
	hashMapA0.put("D-1", "001110");
	hashMapA0.put("A-1", "110010");
	hashMapA0.put("D+A", "000010");
	hashMapA0.put("D-A", "010011");
	hashMapA0.put("A-D", "000111");
	hashMapA0.put("D&A", "000000");
	hashMapA0.put("D|A", "010101");
	HashMap<String, String> hashMapA1 = new HashMap<String, String>();
	hashMapA1.put("M", "110000");
	hashMapA1.put("!M", "110001");
	hashMapA1.put("-M", "110011");
	hashMapA1.put("M+1", "110111");
	hashMapA1.put("M-1", "110010");
	hashMapA1.put("D+M", "000010");
	hashMapA1.put("D-M", "010011");
	hashMapA1.put("M-D", "000111");
	hashMapA1.put("MD", "000000");
	hashMapA1.put("D|M", "010101");
	HashMap<String, String> hashMapDest = new HashMap<String, String>();
	hashMapDest.put(null, "000");
	hashMapDest.put("M", "001");
	hashMapDest.put("D", "010");
	hashMapDest.put("MD", "011");
	hashMapDest.put("A", "100");
	hashMapDest.put("AM", "101");
	hashMapDest.put("AD", "110");
	hashMapDest.put("AMD", "111");
	HashMap<String, String> hashMapJmp = new HashMap<String, String>();
	hashMapJmp.put(null, "000");
	hashMapJmp.put("JGT", "001");
	hashMapJmp.put("JEQ", "010");
	hashMapJmp.put("JGE", "011");
	hashMapJmp.put("JLT", "100");
	hashMapJmp.put("JNE", "101");
	hashMapJmp.put("JLE", "110");
	hashMapJmp.put("JMP", "111");
	
	Scanner reader = new Scanner(System.in);
	System.out.println("Please enter asm file to be translated: ");
	String fileName = reader.next();
	
    try {
        FileReader fileReader = 
            new FileReader(fileName);
        BufferedReader bufferedReader = 
            new BufferedReader(fileReader);

        while((currentLine = bufferedReader.readLine()) != null) {
        	nextLine = "";
        	currentLine = currentLine.trim();		// takes away white space
        	if(currentLine.contains("//"))			// deletes any comments
        	{
        		String[] splitLine = currentLine.split("//");
        		String splitLine1 = splitLine[0];
        		currentLine = splitLine1;
        	}
        	if(!currentLine.isEmpty())				// checks if current line is empty
        	{
//        		System.out.println(currentLine);
        		if(!currentLine.contains("@") && !currentLine.contains(";"))
        		{
            	firstHalf = currentLine.substring(0, currentLine.indexOf("="));
            	secondHalf = currentLine.substring(currentLine.indexOf("=")+1, currentLine.length());
            		if(firstHalf.matches("M\\[(\\d+)\\](.*)")){
            			currentLine =  "@" + firstHalf.substring(firstHalf.indexOf("[")+1, firstHalf.indexOf("]"));
            			nextLine = "M=" + secondHalf;
//            			System.out.println("M=" + nextLine);
            		}
            		else if (secondHalf.substring(0, secondHalf.length()).matches("M\\[(\\d+)\\](.*)")) {
            			
            			nextLine = "D=" + secondHalf;
            			if(secondHalf.indexOf("]") != secondHalf.length()-1)
            			{
//            				System.out.println("LOOK" + currentLine.indexOf("="));
            				nextLine = currentLine.substring(0, currentLine.indexOf("=")) + "=M" + currentLine.substring(currentLine.indexOf("]")+1, currentLine.length());
            			}
            			currentLine = "@" + secondHalf.substring(secondHalf.indexOf("[")+1, secondHalf.indexOf("]"));
//            			System.out.println(nextLine);
            		}
//        		System.out.println(firstHalf + "  =  " + secondHalf);
        		}
	        	char atChar = currentLine.charAt(0);
	        	String numbChar = currentLine.substring(1, currentLine.length());
//	        	System.out.println(atChar + numbChar);
        		if(atChar == '@')
        		{
	        		binaryLineA = "0";
	        		String binaryNumber = Integer.toBinaryString(Integer.parseInt(numbChar));
	        		int filler = 15 - binaryNumber.length();
	        		for(int i = 0; i < filler; i++)
	        		{ 
	        			binaryLineA = binaryLineA + "0";
	        		}
	        		binaryLineA = binaryLineA + binaryNumber;
//	        		System.out.println(currentLine);
	        		System.out.println(binaryLineA);
	        		currentLine = nextLine;
        		}
        		if(currentLine.contains(";") && !currentLine.contains("="))
        		{
        			String dest = "000";
        			String[] CInArr = currentLine.split(";");
        			String compStr = CInArr[0];
        			String jmpStr = CInArr[1];
        			String comp = hashMapA0.get(compStr);
        			String jmp = hashMapJmp.get(jmpStr);
        			binaryLineC = "1110" + comp + dest + jmp;
        			System.out.println(binaryLineC);
        		}
        		if(currentLine.contains("=") && currentLine.contains(";"))
        		{
        			String[] CInArr = currentLine.split("=");
        			String[] CInArr2 = currentLine.split(";");
        			String destStr = CInArr[0];
        			String jmpStr = CInArr2[1];
        			String[] compStrArr = CInArr[1].split(";");
        			String compStr = compStrArr[0];

        			String dest = hashMapDest.get(destStr);
        			String comp = hashMapA0.get(compStr);
        			String jmp = hashMapJmp.get(jmpStr.trim());
        			binaryLineC = "1110" + comp + dest + jmp;
        			System.out.println(binaryLineC);
        		}
        		if(currentLine.contains("=") && !currentLine.contains(";"))
        		{
        			String jmp = "000";
        			String[] CInArr = currentLine.split("=");
        			String destStr = CInArr[0];
        			String compStr = CInArr[1];
        			String comp;
        			String a;
        			if(compStr.matches("M\\[(\\d+)\\](.*)"))
        			{
        				compStr = compStr.replaceAll("(\\[)[^&]*(\\])", "");
        			}
        		
        			if(compStr.contains("M") || compStr.contains("!M") || compStr.contains("-M") || compStr.contains("M+1") || compStr.contains("M-1") || compStr.contains("D+M") || compStr.contains("D-M") || compStr.contains("M-D") || compStr.contains("MD") || compStr.contains("M|D"))
        			
        			{
            			comp = hashMapA1.get(compStr);
            			a = "1";
        			}else{
        				comp = hashMapA0.get(compStr);
        				a = "0";
        			}
        			String dest = hashMapDest.get(destStr);
        			
        			binaryLineC = "111" + a + comp + dest + jmp;
        			System.out.println(binaryLineC);
        		}
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



