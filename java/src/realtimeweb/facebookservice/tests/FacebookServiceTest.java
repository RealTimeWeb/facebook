package realtimeweb.facebookservice.tests;

import static org.junit.Assert.assertNotNull;

import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.util.ArrayList;

import org.junit.Test;

import realtimeweb.facebookservice.FacebookService;
import realtimeweb.facebookservice.domain.Post;
import realtimeweb.stickyweb.EditableCache;
import realtimeweb.stickyweb.exceptions.StickyWebDataSourceNotFoundException;
import realtimeweb.stickyweb.exceptions.StickyWebDataSourceParseException;
import realtimeweb.stickyweb.exceptions.StickyWebInternetException;
import realtimeweb.stickyweb.exceptions.StickyWebInvalidPostArguments;
import realtimeweb.stickyweb.exceptions.StickyWebInvalidQueryString;
import realtimeweb.stickyweb.exceptions.StickyWebLoadDataSourceException;
import realtimeweb.stickyweb.exceptions.StickyWebNotInCacheException;

public class FacebookServiceTest {
	//Need access token with Extended Permission: read_stream; see https://developers.facebook.com/tools/explorer/
	String token = "";	
	FacebookService facebookService = new FacebookService();
	
	private void assertPostNotNull(Post p) {
		assertNotNull(p.getId());
		assertNotNull(p.getFrom());
		assertNotNull(p.getTo());
		assertNotNull(p.getMessage());
		assertNotNull(p.getPicture());
		assertNotNull(p.getLink());
		assertNotNull(p.getVideo());
		assertNotNull(p.getName());
		assertNotNull(p.getDescription());
		assertNotNull(p.getType());
		assertNotNull(p.getCreatedTime());
		assertNotNull(p.getUpdatedTime());
		assertNotNull(p.getLikes());
		assertNotNull(p.getComments());
	}
	
	@Test
	public void testFacebookServiceOnline() {
		
		ArrayList<Post> posts = facebookService.getFeed(10, token);
		for(Post p: posts){
			System.out.println(p);
			assertPostNotNull(p);
		}
	}
	
	@Test
	public void testFacebookServiceCache() {
		EditableCache recording = new EditableCache();
		//recording
			try {
				recording.addData(facebookService.getFeedRequest(10, token));
			} catch (StickyWebNotInCacheException | StickyWebInternetException
					| StickyWebInvalidQueryString
					| StickyWebInvalidPostArguments e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		//saving
			try {
				recording.saveToStream(new FileOutputStream("test-cache.json"));
			} catch (StickyWebDataSourceNotFoundException
					| StickyWebDataSourceParseException
					| StickyWebLoadDataSourceException
					| FileNotFoundException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		//test retrieving from cache
			FacebookService facebookServiceFromCache = new FacebookService("test-cache.json");
			ArrayList<Post> posts = facebookServiceFromCache.getFeed(10, token);
			for(Post p: posts){
				assertPostNotNull(p);
			}
	}
	
	
}
