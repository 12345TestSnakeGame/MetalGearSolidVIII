package applications;

import java.awt.EventQueue;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
import java.util.Collection;
import java.util.Collections;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Set;
import java.util.concurrent.Flow.Publisher;

import javax.swing.AbstractAction;
import javax.swing.Action;
import javax.swing.ButtonGroup;
import javax.swing.ImageIcon;
import javax.swing.JCheckBoxMenuItem;
import javax.swing.JFrame;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JPanel;
import javax.swing.JPopupMenu;
import javax.swing.JRadioButtonMenuItem;
import javax.swing.KeyStroke;

import APIs.CircularObjectAPIs;
import APIs.CircularOrbitHelper;
import applications.builder.AtomCoreBuilder;
import applications.builder.ElectronBuilder;
import applications.builder.PlanetBuilder;
import applications.builder.StellarBuilder;
import centralObject.AtomCore;
import centralObject.CentralObject;
import centralObject.Person;
import centralObject.Stellar;
import circularOrbit.AtomStructure;
import circularOrbit.CircularOrbit;
import circularOrbit.ConcreteCircularOrbit;
import circularOrbit.SocialNetworkCircle;
import circularOrbit.StellarSystem;
import physicalObject.Electron;
import physicalObject.PhysicalObject;
import physicalObject.Planet;
import track.Track;

/*
 *		  			Client 
 * 				      ||
 * 					  ||
 * 		    		  \/
 * 			 choose CircularOrbit
 * 		  || 		    ||   		  ||
 * 		  \/            \/            \/
 *   StellarSystem AtomStructure SocialNetwork
 *   |||||||||||||||||||||||||||||||||||||||||
 *   other applications
 */
public class Client {
	
	//macro
	public static final int STELLAR = 1;
	public static final int ATOM = 2;
	public static final int SOCIAL = 3;

	/*
	 * 
	 */
	private static String[] commandslist = {"help", "create", "add", "delete", "visualize", "transit"
			, "move", "buildrelation", "deleterelation", "get", "is", "has", "concrete"};
	private static Set<String> commands = new HashSet<String>();
	private static String[] concretecommandslist = {"switch", "replace", "create"};
	private static Set<String> concretecommands = new HashSet<String>();
	static {
		Collections.addAll(commands, commandslist);
		Collections.addAll(concretecommands, concretecommandslist);
	}
	
	private CircularOrbitHelper helper;
	private CircularObjectAPIs api;
	private transitMemento transitMemento;
	
	
	public Client() {
		helper = new CircularOrbitHelper();
		Concretes = new LinkedList<CircularOrbit<? extends CentralObject,? extends PhysicalObject>>();
		concretesTypes = new LinkedList<String>();
		api = new CircularObjectAPIs();

	}
	
	public static void main(String args[]) {		
		/*
		
		CircularOrbit<Person, Person> socialNetworkCircularOrbit;
		AbstractFactory<Person, Person> socialNetworkFactory = new SocialNetworkCircleFactory();
		socialNetworkFactory.createConcreteCircularOrbit(new File("data/SocialNetworkCircle.txt"));
		socialNetworkCircularOrbit = socialNetworkFactory.getCircularOrbit();
		System.out.println(socialNetworkCircularOrbit);
		
		*/
		/*
		CircularOrbit<? extends CentralObject,? extends PhysicalObject> concreteCircularOrbit;
		AbstractFactory<AtomCore, Electron> atomStructureFactory= new AtomStructureFactory();
		atomStructureFactory.createConcreteCircularOrbit(new File("data/AtomicStructure_Medium.txt"));
		concreteCircularOrbit = atomStructureFactory.getCircularOrbit();
		System.out.println(concreteCircularOrbit);
		*/
		/*
		CircularOrbit<Stellar, Planet> concreteCircularOrbit;
		AbstractFactory<Stellar, Planet> stellarSystemFactory= new StellarSystemFactory();
		stellarSystemFactory.createConcreteCircularOrbit("test");
		//?????
		concreteCircularOrbit = stellarSystemFactory.getCircularOrbit();
		
		concreteCircularOrbit.readFile(new File("data/StellarSystem_Larger.txt"));
		//TODO complete the iterator
		System.out.println(concreteCircularOrbit.toString());
		*/
		
		Client client = new Client();
		client.createConcrete("StellarSystem");
		client.createConcrete("StellarSystem",new File("data/StellarSystem.txt"));
		client.createConcrete("StellarSystem",new File("data/MyStellarSystemTest-1.txt"));
		
		//visualize test
		//client.parseline("visualize 1");
		
		//get test
		client.parseline("get");
		client.parseline("get track 1");
		client.parseline("get object 2-1");
		client.parseline("get object 3");
		client.parseline("get center");
		client.parseline("get relationgraph");
		client.parseline("get trackcount");
	}

	public List<String> getTypeList(){
		return this.concretesTypes;
	}
	
	/*
	 * the first things to do is to manage concretes
	 * there are two ways of creating a concrete: create an empty one or generate from files
	 * 
	 * the list stores different types of concrete, only one concrete can be on the table at one time
	 */
	
	//current concrete's type
	private String type;
	//current concrete's number
	private int concreteNumber=-1;
	//count existing concretes
	private static int concretesCount=0;
	//exsiting concretes
	private static List<CircularOrbit<? extends CentralObject, ? extends PhysicalObject>> Concretes;
	//record the types of existing concretes
	private static List<String> concretesTypes;
	
	//the current concrete on the table
	private CircularOrbit<? extends CentralObject, ? extends PhysicalObject> concrete;	
	
	StellarSystem concreteStellar;
	AtomStructure concreteAtom;
	SocialNetworkCircle concreteSocial;
	
	/*
	 * manage concretes
	 */
	/*
	 * if there is a concrete on the table
	 * @return if current concrete on the table is not null
	 */
	public boolean hasConcrete() { return concrete!=null; }
	/*
	 * there are three choices right now:
	 * StellarSystem
	 * AtomStructure
	 * SocialNetworkCircle
	 * this method will create an empty concrete
	 * @param the type of concrete to create
	 */
	public void createConcrete(String name) {
		if(name.equalsIgnoreCase("StellarSystem")) {
			concrete = new StellarSystem();
			concreteStellar = (StellarSystem)concrete;
			type = "StellarSystem";
		}else if(name.equalsIgnoreCase("AtomStructure")) {
			concrete = new AtomStructure("default");
			concreteAtom = (AtomStructure)concrete;
			type = "AtomStructure";
		}else if(name.equalsIgnoreCase("SocialNetworkCircle")){
			concrete = new SocialNetworkCircle();
			concreteSocial = (SocialNetworkCircle)concrete;
			type = "SocialNetworkCircle";
		}
		concretesCount++;
		concreteNumber=concretesCount-1;
		Concretes.add(concrete);
		concretesTypes.add(type);//record and store
	}
	/*
	 * there are three choices right now:
	 * StellarSystem
	 * AtomStructure
	 * SocialNetworkCircle
	 * this method will create a concrete implements from files
	 * @param the type of concrete to create
	 * @param the file to generate the concrete
	 */
	public boolean createConcrete(String name, File in) {
		if(name.equalsIgnoreCase("StellarSystem")) {
			concrete = StellarSystem.readFile(in);
			if(concrete==null)return false;
			concreteStellar = (StellarSystem)concrete;
			type = "StellarSystem";
		}else if(name.equalsIgnoreCase("AtomStructure")) {
			concrete = AtomStructure.readFile(in);
			if(concrete==null)return false;
			concreteAtom = (AtomStructure)concrete;
			type = "AtomStructure";
		}else if(name.equalsIgnoreCase("SocialNetworkCircle")){
			concrete = SocialNetworkCircle.readFile(in);
			if(concrete==null)return false;
			concreteSocial = (SocialNetworkCircle)concrete;
			type = "SocialNetworkCircle";
		}
		concretesCount++;
		concreteNumber=concretesCount-1;
		Concretes.add(concrete);
		concretesTypes.add(type);//record and store
		return true;
	}
	/*
	 * implement with a default concrete name
	 */
	/*
	 * @param the number of the concrete to be removed
	 */
	public void removeConcrete(int number) {
		if(number>0||number<=concretesCount)
		{
			if(concrete==Concretes.get(number-1))
			{
				concreteNumber=-1;
				concrete=null;
			}
			concretesCount--;
			if(number<concreteNumber)
				concreteNumber--;
			Concretes.remove(number);
			concretesTypes.remove(number);//remove the concrete
		}
	}
	/*
	 * @param the number of concrete to switch
	 */
	public void switchConcrete(int number) {
		number++;
		if(number>0||number<=concretesCount)
		{
			concrete = Concretes.get(number-1);
			type = concretesTypes.get(number-1);
			if(type.equalsIgnoreCase("StellarSystem"))
			{
				concreteStellar = (StellarSystem)concrete;
			}else if(type.equalsIgnoreCase("AtomStructure"))
			{
				concreteAtom = (AtomStructure)concrete;
			}else if(type.equalsIgnoreCase("SocialNetworkCircle"))
			{
				concreteSocial = (SocialNetworkCircle)concrete;
			}
		}
		else {
			concrete=null;
			concreteNumber=-1;	
		}
	}
	
	public StellarSystem getStellar() { return concreteStellar; }
	public CircularOrbit<? extends CentralObject, ? extends PhysicalObject> getConcrete(int number){
		if(number<0||number>=concretesCount)
			return null;
		return Concretes.get(number);
	}
	/*
	 * operations on the concretes
	 */
	
	public static final int TRACK = 1;
	public static final int CENTER = 2;
	public static final int OBJECT = 3;
	public static final int RELATION = 4;
	
	public static final int DEFAULT = 0;
	public static final int CHOOSE_BY_POSITION = 1;
	public static final int CHOOSE_BY_NAME = 2;
	public static final int CHOOSE_BY_NAMES = 2;
	//add delete |relation center object track
	public boolean add(int TYPE, List<String> params, List<String> position, int Config) {
		if(TYPE==TRACK) {
			return false;//unsupported
		}else if(TYPE==CENTER) {
			if(params.isEmpty())
				return false;
			if(type.equalsIgnoreCase("StellarSystem"))
			{
				//choose by tracknumber
				//use position
				StellarBuilder stellarBuilder = new StellarBuilder();
				Stellar stellar = stellarBuilder.build(params);
				return concreteStellar.setCenter(stellar);			
			}else if(type.equalsIgnoreCase("AtomStructure"))
			{
				AtomCoreBuilder atomCoreBuilder = new AtomCoreBuilder();
				AtomCore atomCore = atomCoreBuilder.build(params);
				return concreteAtom.setCenter(atomCore);
			}else if(type.equalsIgnoreCase("SocialNetworkCircle"))
			{
				//implement search object by name
				//unsupported
				return false;
			}
		}else if(TYPE==OBJECT) {
			if(type.equalsIgnoreCase("StellarSystem"))
			{
				PlanetBuilder builder = new PlanetBuilder();
				Planet planet = builder.build(params);
				return concreteStellar.addObject(planet);
			}else if(type.equalsIgnoreCase("AtomStructure"))
			{
				ElectronBuilder builder = new ElectronBuilder();
				Electron electron = builder.build(params);
				return concreteAtom.addObject(electron);
			}else if(type.equalsIgnoreCase("SocialNetworkCircle"))
			{
				//TODO build relation
				return false;
			}
		}else if(TYPE==RELATION) {
			if(type.equalsIgnoreCase("StellarSystem"))
			{
				if(params.size()!=2)
					return false;
				int i1 = Integer.valueOf(params.get(0));
				int i2 = Integer.valueOf(params.get(1));
				Planet planet1 = concreteStellar.getTrackObjects(i1).get(0);
				Planet planet2 = concreteStellar.getTrackObjects(i2).get(0);
				if(planet1!=null&&planet2!=null) 
					return concreteStellar.buildRelation(planet1, planet2);
				return false;
			}else if(type.equalsIgnoreCase("AtomStructure"))
			{
				return false;
			}else if(type.equalsIgnoreCase("SocialNetworkCircle"))
			{
				if(params.size()!=3)
					return false;
				String name1 = params.get(0);
				String name2 = params.get(1);
				double weight = Double.valueOf(params.get(2));
				if(weight<=0||weight>1)
					return false;
				//TODO 3 inputs
				Person person1 = concreteSocial.getPerson(name1);
				Person person2 = concreteSocial.getPerson(name2);
				
				if(name1==concreteSocial.getCenterName())
					concreteSocial.buildRelation(person2, weight);
				else if(name2==concreteSocial.getCenterName())
					concreteSocial.buildRelation(person1, weight);
				else {
					concreteSocial.buildRelation(person1, person2, weight);
				}
				return true;
			}
		}
		return false;
	}
	public void addRelatedPerson(List<String> params) {
		if(params.size()!=5)
			return;
		String name = params.get(0);
		int age = Integer.valueOf(params.get(1));
		String sex = params.get(2);
		String existingName = params.get(3);
		Person newPerson = new Person(name, age, sex);
		double weight = Double.valueOf(params.get(4));
		Person oldPerson = concreteSocial.getPerson(existingName);
		concreteSocial.buildRelation(newPerson, oldPerson, weight);
	}
	public void delete(int TYPE, List<String> position) {
		if(TYPE==TRACK) {
			if(type.equalsIgnoreCase("StellarSystem"))
			{
				if(position.size()!=1)
					return;
				int trackNumber = Integer.valueOf(position.get(0));
				concreteStellar.deleteTrack(trackNumber);
			}else if(type.equalsIgnoreCase("AtomStructure"))
			{
				if(position.size()!=1)
					return;
				int trackNumber = Integer.valueOf(position.get(0));
				concreteAtom.deleteTrack(trackNumber);
			}else if(type.equalsIgnoreCase("SocialNetworkCircle"))
			{
				if(position.size()!=1)
					return;
				int trackNumber = Integer.valueOf(position.get(0));
				concreteSocial.deleteTrack(trackNumber);
			}
		}else if(TYPE==CENTER) {
			if(type.equalsIgnoreCase("StellarSystem"))
			{
				//unsupported
			}else if(type.equalsIgnoreCase("AtomStructure"))
			{
				//unsupported
			}else if(type.equalsIgnoreCase("SocialNetworkCircle"))
			{
				//unsupported
			}
		}else if(TYPE==OBJECT) {
			if(type.equalsIgnoreCase("StellarSystem"))
			{
				if(position.size()!=1)
					return;
				int trackNumber = Integer.valueOf(position.get(0));
				concreteStellar.deleteTrack(trackNumber);
			}else if(type.equalsIgnoreCase("AtomStructure"))
			{
				if(position.size()!=2)
					return;
				int trackNumber = Integer.valueOf(position.get(0));
				int electrons = Integer.valueOf(position.get(1));
				concreteAtom.deleteObject(new Electron(trackNumber, electrons));
			}else if(type.equalsIgnoreCase("SocialNetworkCircle"))
			{
				if(position.size()!=1)
					return;
				String name = position.get(0);
				Person personssPerson = concreteSocial.getPerson(name);
				concreteSocial.deleteObject(personssPerson);
			}
		}else if(TYPE==RELATION) {
			if(type.equalsIgnoreCase("StellarSystem"))
			{
				if(position.size()!=2)
					return;
				int trackNumber1 = Integer.valueOf(position.get(0));
				int trackNumber2 = Integer.valueOf(position.get(1));
				if(trackNumber1==0) {
					Planet planet2 = concreteStellar.getTrackObjects(trackNumber2).get(0);
					concreteStellar.deleteRelation(planet2);
				}else if(trackNumber2==0) {
					Planet planet1 = concreteStellar.getTrackObjects(trackNumber1).get(0);
					concreteStellar.deleteRelation(planet1);
				}else {
					Planet planet1 = concreteStellar.getTrackObjects(trackNumber1).get(0);
					Planet planet2 = concreteStellar.getTrackObjects(trackNumber2).get(0);
					concreteStellar.deleteRelation(planet1, planet2);	
				}
			}else if(type.equalsIgnoreCase("AtomStructure"))
			{
				//unsupported
			}else if(type.equalsIgnoreCase("SocialNetworkCircle"))
			{
				if(position.size()!=2)
					return;
				String centerString = concreteSocial.getCenterName();
				String name1 = position.get(0);
				String name2 = position.get(1);
				if(name1.equals(centerString)) {
					Person person2 = concreteSocial.getPerson(name2);
					concreteSocial.deleteObject(person2);
				}else if(name2.equals(centerString)) {
					Person person1 = concreteSocial.getPerson(name1);
					concreteSocial.deleteRelation(person1);
				}else {
					Person person1 = concreteSocial.getPerson(name1);
					Person person2 = concreteSocial.getPerson(name2);
					concreteSocial.deleteRelation(person1, person2);
				}
			}
		}
	}
	
	/*
	 * other APIs and calculations on the concretes, visualize
	 */
	//transit entropy distance difference
	public boolean transit(List<String> params) {
		if(params.size()!=3)
			return false;
		int track1 = Integer.valueOf(params.get(0));
		int track2 = Integer.valueOf(params.get(1));
		int number = Integer.valueOf(params.get(2));
		return concreteAtom.transit(track1, track2, number);
	}
	public double getPhysicalDistance(List<String> params) {
		if(params.size()!=2)
			return -1;
		int track1 = Integer.valueOf(params.get(0));
		int track2 = Integer.valueOf(params.get(1));
		return concreteStellar.getPhysicalDistance(track1, track2);
	}
	public double getSpread(List<String> params) {
		if(params.size()!=1)
			return 0;
		String name = params.get(0);
		return concreteSocial.getSpread(concreteSocial.getPerson(name));
	}
	public int getLogicalDistance(List<String> params) {
		if(params.size()!=2)
			return -1;
		String name1 = params.get(0);
		String name2 = params.get(1);
		Person person1 = concreteSocial.getPerson(name1);
		Person person2 = concreteSocial.getPerson(name2);
		
		return concreteSocial.getDistance(person1, person2);
	}
	public double getEntropy() { return api.getObjectDistributionEntropy(concrete); }
	public void visualize() { //in the GUI 
		}
	public void moveFor(List<String> params) {
		if(params.size()!=1)
			return;
		double year1 = Double.valueOf(params.get(0));
		concreteStellar.revolutionFor(year1);
	}
	public void moveTo(List<String> params) {
		if(params.size()!=1)
			return;
		double year1 = Double.valueOf(params.get(0));
		concreteStellar.revolutionTo(year1);
	}
	public void transitWIthMemento(List<String> params) {
		transit(params);
		transitMemento = new transitMemento("default");
		if(params.size()!=3)
			return;
		int track1 = Integer.valueOf(params.get(0));
		int track2 = Integer.valueOf(params.get(1));
		int number = Integer.valueOf(params.get(2));
		transitMemento.getMemento(track1, track2, number);
	}
	public void reTransitfromMemento() {
		concreteAtom.setMemento();
	}
	public String getDifference(List<String> params) {
		if(params.size()!=2)
			return "failed";
		int concrete1 = Integer.valueOf(params.get(0));
		int concrete2 = Integer.valueOf(params.get(1));
		CircularOrbit<? extends CentralObject,? extends PhysicalObject> c1 = getConcrete(concrete1);
		CircularOrbit<? extends CentralObject,? extends PhysicalObject> c2 = getConcrete(concrete2);
		return api.getDifference(c1, c2).toString();
	}
	
	/*
	 * getters
	 */
	public static final int NAMES = 1;
	public static final int NUMBERS = 2;
	public static final int POSITIONS = 3;
	public static final int INFORMATIONS = 4;
	//get |numbers, names, and other information
	public void get(int TYPE, List<String> params) {
		
	}
	public double getDouble(List<String> params) {
		return 1;
	}
	public int getInteger(List<String> params) {
		return 0;
	}
	public String getString(List<String> params) {
		return "";
	}
	
	/*
	 * judges
	 */
	
	public void parseline(String input) {
		//-concrete switch-
		//concrete replace
		//-concrete create-
		//======================================
		//create [type] [file]* [name]*
		//add [track]*
		//delete [track|object] [number|object number]
		//help (print help info)
		//-visualize
		//transit-AtomStructure
		//move-StellarSystem
		//buildrelation
		//deleterelation
		//getters
		//  APIs getEntropy
		//  	 getLogicalDistance
		//  	 getPhysicalDistance
		//  	 getDifference
		// - get
		// -	 track&objects-
		// -	 center-
		//	is/has 
		//		 hasPosition...
		//  
		/*
		 * get rules:
		 * get [track|center|object]  	
		 */
		String[] inputs = input.split("\\s+");
		
		//illegal input
		if(inputs.length==0)
			return;
		if(!commands.contains(inputs[0]))
		{
			outPut(help(""));
		}
		else if(inputs[0].equalsIgnoreCase("help")) {
			outPut(help(inputs[1]));
		}
		else if(inputs[0].equalsIgnoreCase("get")) {
			if(!hasConcrete())
			{
				outPut("please create or choose a concrete circular orbit!");
				outPut(help("concrete"));
			}
			if(inputs.length<2)
				outPut(help(""));
			else
			getters(inputs);
			
		}else if(inputs[0].equalsIgnoreCase("concrete")) {
			if(inputs.length<2)
				outPut(help("concrete"));
			if(!concretecommands.contains(inputs[1]))
				outPut(help("concrete"));
			if(inputs[1].equalsIgnoreCase("switch")) {
				 if(inputs.length<3)
					 outPut(help("concrete"));
				 else {
					int number = Integer.valueOf(inputs[2]);
					if(number>0&&number<=concretesCount)
						concrete = Concretes.get(number+1);
				}
			}else if(inputs[1].equalsIgnoreCase("replace")) {
				
			}else if(inputs[1].equalsIgnoreCase("create")) {
				if(inputs.length==2)
					outPut(help("concrete"));
				else if(inputs.length==3)
				{
					createConcrete(inputs[2]);
				}else if(inputs.length==4)
				{
					createConcrete(inputs[2], new File("data/"+inputs[3]));
				}
			}
		}else if(inputs[0].equalsIgnoreCase("")) {
			if(!hasConcrete())
			{
				outPut("please create or choose a concrete circular orbit!");
				outPut(help("concrete"));
			}
			if(inputs.length<2)
				outPut(help(""));
		}else if(inputs[0].equalsIgnoreCase("")) {
			if(!hasConcrete())
			{
				outPut("please create or choose a concrete circular orbit!");
				outPut(help("concrete"));
			}
			if(inputs.length<2)
				outPut(help(""));
		}else if(inputs[0].equalsIgnoreCase("")) {
			if(!hasConcrete())
			{
				outPut("please create or choose a concrete circular orbit!");
				outPut(help("concrete"));
			}
			if(inputs.length<2)
				outPut(help(""));
		}else if(inputs[0].equalsIgnoreCase("visualize")) {
			if(!hasConcrete()&&inputs.length<2)
			{
				outPut("please create or choose a concrete circular orbit!");
				outPut(help("concrete"));
			}
			if(inputs.length==1)
			{
				CircularOrbitHelper.visualize(concrete, 1);
			}
			else {
				int number = Integer.valueOf(inputs[1]);
				if(number>0&&number<=concretesCount)
					CircularOrbitHelper.visualize(Concretes.get(number-1), 1);
			}
		}
		
	}
	public void APIs() {
		
	}
	public String getters(String[] inputs) {
		String choice1 = inputs[1];
		if(choice1.equalsIgnoreCase("center")) {
			outPut(concrete.getCenterName());
		}else if(choice1.equalsIgnoreCase("relationgraph")) {
			outPut(concrete.getGraph().toString());
		}else if(choice1.equalsIgnoreCase("trackcount")) {
			outPut(Integer.valueOf(concrete.getTrackNumber()).toString());
		}else {
			if(inputs.length<3)
				outPut(help(""));
			if(choice1.equalsIgnoreCase("track"))
			{
				int trackNumber = Integer.valueOf(inputs[2]);
				try {
					outPut(concrete.getTrackObjects(trackNumber).toString());
				} catch (Exception e) {
					e.printStackTrace();
				}
			}else if(choice1.equalsIgnoreCase("object")) {
				String[] indexStrings = inputs[2].split("-");
				if(indexStrings.length==1)
				{
					int number = Integer.valueOf(indexStrings[0]);
					outPut(concrete.getObject(number).toString());
				}if(indexStrings.length==2) {
					int tracknum = Integer.valueOf(indexStrings[0]);
					int num = Integer.valueOf(indexStrings[1]);
					try {
						outPut(concrete.getTrackObjects(tracknum).get(num-1).toString());
					} catch (Exception e) {
						e.printStackTrace();
					}
				}
			}
		}
		return null;
	}
	public boolean isnhas() {
		return false;
	}
	public String help(String choice) {
		List<String> getters = new LinkedList<String>();
		String get_rules = "get [track|center|object|relationgraph|trackcount|] [(track number)|(object number)|(track-object number)]";
		String get_pl = "\"get object 3-2\" or \"get track 4\"";
		
		String visualize_rules = "visualize [concrete number]*";
		String visualizs_rules2 = "if input visualize only, the defualt operation is to visualize current concrete";
		return null;
	}
	
	public void show() { System.out.println(concrete); }
	public String circularOrbitType() {return this.type;}
	public void outPut(String information) { System.out.println(information); }


}	

class transitMemento{
	public boolean transited;
	private int sourceTrack;
	private int targetTrack;
	private int number;
	private String name;
	public transitMemento(String name) {
		this.name=name;
	}
	
	public void getMemento(int sourceTrack, int targetTrack, int number) {
		this.sourceTrack=sourceTrack;
		this.targetTrack=targetTrack;
		this.number=number;
		transited=true;
	}
	public void setMemento(AtomStructure atomStructure) {
		atomStructure.transit(targetTrack, sourceTrack, -number);
		transited=false;
	}
	
}
