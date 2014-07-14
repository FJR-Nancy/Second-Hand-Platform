package zju.secondhandplatform.client;

import android.app.Activity;
import android.app.Fragment;
import android.content.Intent;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

	/**
     * A placeholder fragment containing a simple view.
     */
public class PersonalInfo extends Fragment {
        /**
         * The fragment argument representing the section number for this
         * fragment.
         */
        private static final String ARG_SECTION_NUMBER = "section_number";

        /**
         * Returns a new instance of this fragment for the given section
         * number.
         */
        public static PersonalInfo newInstance(int sectionNumber) {
            PersonalInfo fragment = new PersonalInfo();
            Bundle args = new Bundle();
            args.putInt(ARG_SECTION_NUMBER, sectionNumber);
            fragment.setArguments(args);
            return fragment;
        }

        public PersonalInfo() {
        }

        @Override
        public View onCreateView(LayoutInflater inflater, ViewGroup container,
                Bundle savedInstanceState) {
            View rootView = inflater.inflate(R.layout.fragment_personal_info, container, false);

            ClientApp clientApp=(ClientApp)getActivity().getApplicationContext();
        	if(clientApp.getId()==-1){       		
        		try{
        			Intent intent = new Intent();
        			intent.setClass(getActivity(), Login.class);
        			startActivity(intent);
        		}catch(Exception e){
        			e.printStackTrace();
        		}        	
        	}
        	else{
        		
        	}
        	
            return rootView;
        }

        @Override
        public void onAttach(Activity activity) {
            super.onAttach(activity);
            ((MainActivity) activity).onSectionAttached(
                    getArguments().getInt(ARG_SECTION_NUMBER));
        }
    }
