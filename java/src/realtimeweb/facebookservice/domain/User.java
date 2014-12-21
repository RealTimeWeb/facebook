package realtimeweb.facebookservice.domain;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;




/**
 * A user represents a person on Facebook.
 */
public class User {
	
    // https://developers.facebook.com/docs/graph-api/reference/v2.2/user
    
    private String id;
    private String name;
    
    
    /*
     * @return The id of this person's user account.
     */
    public String getId() {
        return this.id;
    }
    
    /*
     * @param The id of this person's user account.
     * @return String
     */
    public void setId(String id) {
        this.id = id;
    }
    
    /*
     * @return The person's full name
     */
    public String getName() {
        return this.name;
    }
    
    /*
     * @param The person's full name
     * @return String
     */
    public void setName(String name) {
        this.name = name;
    }
    
	
	/**
	 * Creates a string based representation of this User.
	
	 * @return String
	 */
	public String toString() {
		return "User[" +id+", "+name+"]";
	}
	
	/**
	 * Internal constructor to create a User from a json representation.
	 * @param map The raw json data that will be parsed.
	 * @return 
	 */
    public User(Map<String, Object> raw) {
        // TODO: Check that the data has the correct schema.
        // NOTE: It's much safer to check the Map for fields than to catch a runtime exception.
        try {
            this.id = raw.get("id").toString();
            this.name = raw.get("name").toString();
        } catch (NullPointerException e) {
    		System.err.println("Could not convert the response to a User; a field was missing.");
    		e.printStackTrace();
    	} catch (ClassCastException e) {
    		System.err.println("Could not convert the response to a User; a field had the wrong structure.");
    		e.printStackTrace();
        }
    
	}	
}