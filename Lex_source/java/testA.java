package applications;

import java.io.*;
import java.util.ArrayList;
import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import centralObject.Stellar;
import circularOrbit.StellarSystem;

public class testA {
	public static void main(String args[]) {
		
		StellarSystem OurStellar;
		
		String labelRegex = "[a-zA-Z0-9]+";
		String wordRegex = "[a-zA-Z]+";
		//the space cannot be at the start of a sentence?
		String sentenceRegex = "[a-zA-Z0-9\\s]+";
		//number regex:
		//integer <10000 [0-9]{1,4}
		//double <10000 [0-9]{1,4}\.[0-9]+
		//sci [1-9]\.([0-9]+)e[3-9][0-9]+
		String integerRegex = "[0-9]{1,4}";
		String doubleRegex = "([0-9]{1,4})\\.[0-9]+";
		String sciRegex = "[1-9](\\.[0-9]+)?e([3-9][0-9]*|[1-9][0-9]+)";
		String numberRegex = "("+integerRegex+"|"+doubleRegex+"|"+sciRegex+")";
		String revolutionDirectioinRegex = "(CCW|CW)";
		String angleRegex = "[0-9]{1,3}(\\.[0-9]+)?";
		
		String stellarRegex = "Stellar ::= <"+labelRegex+","+numberRegex+","+numberRegex+">";
		String planetRegex = "Planet ::= <" +labelRegex+","
											+labelRegex+","
											+labelRegex+","
											+numberRegex+","
											+numberRegex+","
											+numberRegex+","
											+revolutionDirectioinRegex+","
											+angleRegex+">";
		File read1 = new File("data/StellarSystem-1.txt");
		
		ArrayList<String> sentenceStrings = new ArrayList<String>();
		
		ArrayList<String> stellars = new ArrayList<String>();
		ArrayList<String> planets = new ArrayList<String>();
		
		if(read1.isFile()&&read1.exists()) 
		{
			try 
			{
				Scanner readFile = new Scanner(read1);
				while(readFile.hasNextLine()) 
				{
					sentenceStrings.add(readFile.nextLine());
				}
			}
			catch (Exception e) 
			{
				// TODO: handle exception
				e.printStackTrace();
			}
		}
		System.out.println(sentenceStrings);
		
		Pattern stellarPattern =Pattern.compile(stellarRegex);
		for(String test:sentenceStrings) 
		{
			Matcher testoftest = stellarPattern.matcher(test);
			if(testoftest.find())
			{
				System.out.println(test);
				stellars.add(test);
			}
			else {
				//System.out.println("regex match failed");
				//System.out.println();
			}
		}
		
		System.out.println();
		Pattern planetPattern =Pattern.compile(planetRegex);
		for(String test:sentenceStrings) 
		{
			Matcher testoftest = planetPattern.matcher(test);
			if(testoftest.find())
			{
				//System.out.println(test);
				planets.add(test);
			}
			else {
				System.out.println("regex match failed");
				System.out.println(test);
				System.out.println();
			}
		}
	}
}
