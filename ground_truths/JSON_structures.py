topics_of_interest_string = """
    "topics_your_topics": [
        {
            "media_map_data": {},
            "string_map_data": {
                "Name": {
                    "href": "str",
                    "timestamp": "int",
                    "value": "str"
                }
            },
            "title": "str"
        }
    ]
"""

ads_analysis_string = """
    "impressions_history_ads_seen": [
        {
            "string_map_data": {
                "Author": {
                    "value": "str"
                },
                "Time": {
                    "timestamp": "int"
                }
            }
        }
    ]
"""

daily_weekly_views_string = """
    "impressions_history_posts_seen": [
        {
            "string_map_data": {
                "Author": {
                    "value": "str"
                },
                "Time": {
                    "timestamp": "int"
                }
            }
        }
    ]
"""

company_access_string = """
    "ig_custom_audiences_all_types": [
        {
            "advertiser_name": "str",
            "has_data_file_custom_audience": "bool",
            "has_in_person_store_visit": "bool",
            "has_remarketing_custom_audience": "bool"
        }
    ]
"""

device_logins = """
    "devices_devices": [
        {
            "media_map_data": {},
            "string_map_data": {
                "Last Login": {
                    "href": "str",
                    "timestamp": "int",
                    "value": "str"
                },
                "User Agent": {
                    "href": "str",
                    "timestamp": "int",
                    "value": "str"
                }
            },
            "title": "str"
        }
    ]
"""

account_changes_string = """
    "profile_profile_change": [
        {
            "media_map_data": {},
            "string_map_data": {
                "Change Date": {
                    "href": "str",
                    "timestamp": "int",
                    "value": "str"
                },
                "Changed": {
                    "href": "str",
                    "timestamp": "int",
                    "value": "str"
                },
                "New Value": {
                    "href": "str",
                    "timestamp": "int",
                    "value": "str"
                },
                "Previous Value": {
                    "href": "str",
                    "timestamp": "int",
                    "value": "str"
                }
            },
            "title": "str"
        }
    ]
"""

story_engagements_string = """
    "story_activities_emoji_sliders": [
        {
            "string_list_data": [
                {
                    "timestamp": "int",
                    "value": "str"
                }
            ],
            "title": "str"
        }
    ],
    "story_activities_emoji_quick_reactions": [
        {
            "media_list_data": [],
            "string_list_data": [
                {
                    "href": "str",
                    "timestamp": "int",
                    "value": "str"
                }
            ],
            "title": "str"
        }
    ],
    "story_activities_polls": [
        {
            "string_list_data": [
                {
                    "timestamp": "int",
                    "value": "str"
                }
            ],
            "title": "str"
        }
    ],
     "story_activities_questions": [
        {
            "media_list_data": [],
            "string_list_data": [
                {
                    "href": "str",
                    "timestamp": "int",
                    "value": "str"
                }
            ],
            "title": "str"
        }
    ],
    "story_activities_quizzes": [
        {
            "string_list_data": [
                {
                    "timestamp": "int",
                    "value": "str"
                }
            ],
            "title": "str"
        }
    ],
    "story_activities_story_likes": [
        {
            "string_list_data": [
                {
                    "timestamp": "int"
                }
            ],
            "title": "str"
        }
    ],
    "story_activities_reaction_sticker_reactions": [
        {
            "media_list_data": [],
            "string_list_data": [
                {
                    "href": "str",
                    "timestamp": "int",
                    "value": "str"
                }
            ],
            "title": "str"
        }
    ]
"""

top_interactions_string = """
    "likes_media_likes": [
        {
            "string_list_data": [
                {
                    "href": "str",
                    "timestamp": "int",
                    "value": "str"
                }
            ],
            "title": "str"
        }
    ],
     "story_activities_story_likes": [
        {
            "string_list_data": [
                {
                    "timestamp": "int"
                }
            ],
            "title": "str"
        }
    ],
    "comments_reels_comments": [
        {
            "string_map_data": {
                "Comment": {
                    "value": "str"
                },
                "Media Owner": {
                    "value": "str"
                },
                "Time": {
                    "timestamp": "int"
                }
            }
        }
    ]
"""

followers_and_following = """
    {
        "media_list_data": [],
        "string_list_data": [
            {
                "href": "str",
                "timestamp": "int",
                "value": "str"
            }
        ],
        "title": "str"
    },
    "relationships_following": [
        {
            "media_list_data": [],
            "string_list_data": [
                {
                    "href": "str",
                    "timestamp": "int",
                    "value": "str"
                }
            ],
            "title": "str"
        }
    ]
"""

posts_and_videos_string = """
    "impressions_history_posts_seen": [
        {
            "string_map_data": {
                "Author": {
                    "value": "str"
                },
                "Time": {
                    "timestamp": "int"
                }
            }
        }
    ],
     "impressions_history_videos_watched": [
        {
            "string_map_data": {
                "Author": {
                    "value": "str"
                },
                "Time": {
                    "timestamp": "int"
                }
            }
        }
    ]
"""

viewed_not_liked_string = """
    "impressions_history_posts_seen": [
        {
            "string_map_data": {
                "Author": {
                    "value": "str"
                },
                "Time": {
                    "timestamp": "int"
                }
            }
        }
    ],
    "likes_media_likes": [
        {
            "string_list_data": [
                {
                    "href": "str",
                    "timestamp": "int",
                    "value": "str"
                }
            ],
            "title": "str"
        }
    ]
"""

weekly_messages_string = """
    "messages": [
        {
          "sender_name": "str",
          "timestamp_ms": "int",
          "content": "str",
          "is_geoblocked_for_viewer": "bool",
          "is_unsent_image_by_messenger_kid_parent": "bool"
        }
    ]
"""
