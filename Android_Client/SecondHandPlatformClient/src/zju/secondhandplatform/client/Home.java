package zju.secondhandplatform.client;

import java.util.ArrayList;
import java.util.List;

import org.apache.http.NameValuePair;
import org.apache.http.message.BasicNameValuePair;

import android.app.Activity;
import android.app.Fragment;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

	/**
     * A placeholder fragment containing a simple view.
     */
public class Home extends Fragment {
        /**
         * The fragment argument representing the section number for this
         * fragment.
         */
        private static final String ARG_SECTION_NUMBER = "section_number";

        /**
         * Returns a new instance of this fragment for the given section
         * number.
         */
        public static Home newInstance(int sectionNumber) {
            Home fragment = new Home();
            Bundle args = new Bundle();
            args.putInt(ARG_SECTION_NUMBER, sectionNumber);
            fragment.setArguments(args);
            return fragment;
        }

        public Home() {        	
        	List<NameValuePair> params = new ArrayList<NameValuePair>();
    		params.add(new BasicNameValuePair("name", "test"));
    		params.add(new BasicNameValuePair("email", "12345678@qq.com"));
    		params.add(new BasicNameValuePair("password", "123456"));
    		params.add(new BasicNameValuePair("phone", "12345678910"));

    		Json json=new Json("/json_api/add_account/",params);
        }

        @Override
        public View onCreateView(LayoutInflater inflater, ViewGroup container,
                Bundle savedInstanceState) {
            View rootView = inflater.inflate(R.layout.fragment_home, container, false);
            TextView textView = (TextView) rootView.findViewById(R.id.section_label);
 //           textView.setText(Integer.toString(getArguments().getInt(ARG_SECTION_NUMBER)));
            textView.setText("This is home");
            return rootView;
        }

        @Override
        public void onAttach(Activity activity) {
            super.onAttach(activity);
            ((MainActivity) activity).onSectionAttached(
                    getArguments().getInt(ARG_SECTION_NUMBER));
        }
    }
