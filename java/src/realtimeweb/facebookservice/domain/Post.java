package realtimeweb.facebookservice.domain;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;








import realtimeweb.facebookservice.domain.User;

/**
 * An individual entry in a User's feed.
 */
public class Post {
	
    // https://developers.facebook.com/docs/graph-api/reference/v2.2/post
    
    private String id;
    private User from;
    private ArrayList<User> to;
    private String message;
    private String picture;
    private String link;
    private String video;
    private String name;
    private String description;
    private String type;
    private String createdTime;
    private String updatedTime;
    private ArrayList<User> likes;
    private ArrayList<Comment> comments;
    
    
    /*
     * @return The post ID
     */
    public String getId() {
        return this.id;
    }
    
    /*
     * @param The post ID
     * @return String
     */
    public void setId(String id) {
        this.id = id;
    }
    
    /*
     * @return Information about the User that posted the message.
     */
    public User getFrom() {
        return this.from;
    }
    
    /*
     * @param Information about the User that posted the message.
     * @return User
     */
    public void setFrom(User from) {
        this.from = from;
    }
    
    /*
     * @return Users mentioned or targeted in this post.
     */
    public ArrayList<User> getTo() {
        return this.to;
    }
    
    /*
     * @param Users mentioned or targeted in this post.
     * @return ArrayList<User>
     */
    public void setTo(ArrayList<User> to) {
        this.to = to;
    }
    
    /*
     * @return The main body of the post, otherwise called the status message.
     */
    public String getMessage() {
        return this.message;
    }
    
    /*
     * @param The main body of the post, otherwise called the status message.
     * @return String
     */
    public void setMessage(String message) {
        this.message = message;
    }
    
    /*
     * @return The picture scraped from any link included with the post.
     */
    public String getPicture() {
        return this.picture;
    }
    
    /*
     * @param The picture scraped from any link included with the post.
     * @return String
     */
    public void setPicture(String picture) {
        this.picture = picture;
    }
    
    /*
     * @return The link attached to this post.
     */
    public String getLink() {
        return this.link;
    }
    
    /*
     * @param The link attached to this post.
     * @return String
     */
    public void setLink(String link) {
        this.link = link;
    }
    
    /*
     * @return A URL to any Flash movie or video file attached to the post.
     */
    public String getVideo() {
        return this.video;
    }
    
    /*
     * @param A URL to any Flash movie or video file attached to the post.
     * @return String
     */
    public void setVideo(String video) {
        this.video = video;
    }
    
    /*
     * @return The name of the link.
     */
    public String getName() {
        return this.name;
    }
    
    /*
     * @param The name of the link.
     * @return String
     */
    public void setName(String name) {
        this.name = name;
    }
    
    /*
     * @return A description of a link in the post (appears beneath the caption).
     */
    public String getDescription() {
        return this.description;
    }
    
    /*
     * @param A description of a link in the post (appears beneath the caption).
     * @return String
     */
    public void setDescription(String description) {
        this.description = description;
    }
    
    /*
     * @return A string indicating the object type of this post.
     */
    public String getType() {
        return this.type;
    }
    
    /*
     * @param A string indicating the object type of this post.
     * @return String
     */
    public void setType(String type) {
        this.type = type;
    }
    
    /*
     * @return The time the post was initially published.
     */
    public String getCreatedTime() {
        return this.createdTime;
    }
    
    /*
     * @param The time the post was initially published.
     * @return String
     */
    public void setCreated_Time(String created_Time) {
        this.createdTime = created_Time;
    }
    
    /*
     * @return The time of the last change to this post, or the comments on it.
     */
    public String getUpdatedTime() {
        return this.updatedTime;
    }
    
    /*
     * @param The time of the last change to this post, or the comments on it.
     * @return String
     */
    public void setUpdated_Time(String updated_Time) {
        this.updatedTime = updated_Time;
    }
    
    /*
     * @return People who like this post.
     */
    public ArrayList<User> getLikes() {
        return this.likes;
    }
    
    /*
     * @param People who like this post.
     * @return ArrayList<User>
     */
    public void setLikes(ArrayList<User> likes) {
        this.likes = likes;
    }
    
    /*
     * @return Comments on this post.
     */
    public ArrayList<Comment> getComments() {
        return this.comments;
    }
    
    /*
     * @param Comments on this post.
     * @return ArrayList<Comment>
     */
    public void setComments(ArrayList<Comment> comments) {
        this.comments = comments;
    }
    
	
	/**
	 * Creates a string based representation of this Post.
	
	 * @return String
	 */
    public String toString() {
		return "Post[" +id+", "+from+", "+to+", "+message+", "+picture+", "+link+", "+video+", "+name+", "+description+", "+type+", "+createdTime+", "+updatedTime+", "+likes+", "+comments+"]";
	}
	
	/**
	 * Internal constructor to create a Post from a json representation.
	 * @param map The raw json data that will be parsed.
	 * @return 
	 */
    public Post(Map<String, Object> raw) {
        // TODO: Check that the data has the correct schema.
        // NOTE: It's much safer to check the Map for fields than to catch a runtime exception.
        try {
            this.id = raw.get("id").toString();
            this.from = new User((Map<String, Object>)raw.get("from"));
            this.to = new ArrayList<User>();
            
            Map<String, Object> to = (Map<String, Object>) raw.get("to");
            if(to!=null){
            	Iterator<Object> toIter = ((List<Object>)((Map<String, Object>) raw.get("to")).get("data")).iterator();
                while (toIter.hasNext()) {
                    this.to.add(new User((Map<String, Object>)toIter.next()));
                }
            }
            if(raw.get("message") != null){this.message = raw.get("message").toString();} else{this.message="";};
            if(raw.get("picture") != null){this.picture = raw.get("picture").toString();} else{this.picture="";};
            if(raw.get("link") != null){this.link = raw.get("link").toString();} else{this.link="";};
            if(raw.get("source") != null){this.video = raw.get("source").toString();} else{this.video="";};
            if(raw.get("name") != null){this.name = raw.get("name").toString();} else{this.name="";};
            if(raw.get("description") != null){this.description = raw.get("description").toString();} else{this.description="";};
            if(raw.get("type") != null){this.type = raw.get("type").toString();} else{this.type="";};
            if(raw.get("created_time") != null){this.createdTime = raw.get("created_time").toString();} else{this.createdTime="";};
            if(raw.get("updated_time") != null){this.updatedTime = raw.get("updated_time").toString();} else{this.updatedTime="";};
            
            this.likes = new ArrayList<User>();
            if((Map<String, Object>) raw.get("likes")!=null){
	            Iterator<Object> likesIter = ((List<Object>)((Map<String, Object>) raw.get("likes")).get("data")).iterator();
	            while (likesIter.hasNext()) {
	                this.likes.add(new User((Map<String, Object>)likesIter.next()));
	            }
            }
            
            this.comments = new ArrayList<Comment>();
            if((Map<String, Object>) raw.get("comments")!=null){
	        	  Iterator<Object> commentsIter = ((List<Object>)((Map<String, Object>) raw.get("comments")).get("data")).iterator();
	              while (commentsIter.hasNext()) {
	                  this.comments.add(new Comment((Map<String, Object>)commentsIter.next()));
	              }
            }
          
        } catch (NullPointerException e) {
    		System.err.println("Could not convert the response to a Post; a field was missing.");
    		e.printStackTrace();
    	} catch (ClassCastException e) {
    		System.err.println("Could not convert the response to a Post; a field had the wrong structure.");
    		e.printStackTrace();
        }
    
	}	
}