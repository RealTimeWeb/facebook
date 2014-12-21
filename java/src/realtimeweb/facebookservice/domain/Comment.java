package realtimeweb.facebookservice.domain;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;




import realtimeweb.facebookservice.domain.User;

/**
 * A comment to a post.
 */
public class Comment {
	
    // https://developers.facebook.com/docs/graph-api/reference/v2.2/comment
    
    private String id;
    private User from;
    private String message;
    
    
    /*
     * @return The comment ID
     */
    public String getId() {
        return this.id;
    }
    
    /*
     * @param The comment ID
     * @return String
     */
    public void setId(String id) {
        this.id = id;
    }
    
    /*
     * @return The person that made this comment
     */
    public User getFrom() {
        return this.from;
    }
    
    /*
     * @param The person that made this comment
     * @return User
     */
    public void setFrom(User from) {
        this.from = from;
    }
    
    /*
     * @return The comment text
     */
    public String getMessage() {
        return this.message;
    }
    
    /*
     * @param The comment text
     * @return String
     */
    public void setMessage(String message) {
        this.message = message;
    }
    
	
	/**
	 * Creates a string based representation of this Comment.
	
	 * @return String
	 */
	public String toString() {
		return "Comment[" +id+", "+from+", "+message+"]";
	}
	
	/**
	 * Internal constructor to create a Comment from a json representation.
	 * @param map The raw json data that will be parsed.
	 * @return 
	 */
    public Comment(Map<String, Object> raw) {
        // TODO: Check that the data has the correct schema.
        // NOTE: It's much safer to check the Map for fields than to catch a runtime exception.
        try {
            this.id = raw.get("id").toString();
            this.from = new User((Map<String, Object>)raw.get("from"));
            this.message = raw.get("message").toString();
        } catch (NullPointerException e) {
    		System.err.println("Could not convert the response to a Comment; a field was missing.");
    		e.printStackTrace();
    	} catch (ClassCastException e) {
    		System.err.println("Could not convert the response to a Comment; a field had the wrong structure.");
    		e.printStackTrace();
        }
    
	}	
}