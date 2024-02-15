PGDMP     )    	    	            |            domino %   12.11 (Ubuntu 12.11-0ubuntu0.20.04.1) %   12.11 (Ubuntu 12.11-0ubuntu0.20.04.1) Q   L           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            M           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            N           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            O           1262    97058    domino    DATABASE     l   CREATE DATABASE domino WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'es_CU' LC_CTYPE = 'es_CU';
    DROP DATABASE domino;
                postgres    false                        2615    97059 
   enterprise    SCHEMA        CREATE SCHEMA enterprise;
    DROP SCHEMA enterprise;
                postgres    false            P           0    0    SCHEMA enterprise    COMMENT     7   COMMENT ON SCHEMA enterprise IS 'Gestion de usuarios';
                   postgres    false    5            
            2615    97060    events    SCHEMA        CREATE SCHEMA events;
    DROP SCHEMA events;
                postgres    false                        2615    97061    notifications    SCHEMA        CREATE SCHEMA notifications;
    DROP SCHEMA notifications;
                postgres    false            	            2615    97062    post    SCHEMA        CREATE SCHEMA post;
    DROP SCHEMA post;
                postgres    false                        2615    97063 	   resources    SCHEMA        CREATE SCHEMA resources;
    DROP SCHEMA resources;
                postgres    false            �            1259    97064    profile_default_user    TABLE     /  CREATE TABLE enterprise.profile_default_user (
    profile_id character varying NOT NULL,
    sex character varying(1),
    birthdate date,
    alias character varying(30),
    job character varying(120),
    city_id integer,
    updated_by character varying NOT NULL,
    updated_date date NOT NULL
);
 ,   DROP TABLE enterprise.profile_default_user;
    
   enterprise         heap    postgres    false    5            Q           0    0 #   COLUMN profile_default_user.city_id    COMMENT     a   COMMENT ON COLUMN enterprise.profile_default_user.city_id IS 'City to which the player belongs';
       
   enterprise          postgres    false    207            �            1259    97070    profile_event_admon    TABLE     �   CREATE TABLE enterprise.profile_event_admon (
    profile_id character varying NOT NULL,
    updated_by character varying NOT NULL,
    updated_date date NOT NULL
);
 +   DROP TABLE enterprise.profile_event_admon;
    
   enterprise         heap    postgres    false    5            �            1259    97076    profile_followers    TABLE     O  CREATE TABLE enterprise.profile_followers (
    profile_id character varying NOT NULL,
    username character varying NOT NULL,
    profile_follow_id character varying NOT NULL,
    username_follow character varying NOT NULL,
    created_by character varying NOT NULL,
    created_date date NOT NULL,
    is_active boolean NOT NULL
);
 )   DROP TABLE enterprise.profile_followers;
    
   enterprise         heap    postgres    false    5            �            1259    97082    profile_member    TABLE     �  CREATE TABLE enterprise.profile_member (
    id character varying NOT NULL,
    profile_type character varying NOT NULL,
    name character varying(300) NOT NULL,
    email character varying(300),
    photo character varying(255),
    city_id integer,
    created_by character varying NOT NULL,
    created_date date NOT NULL,
    updated_by character varying NOT NULL,
    updated_date date NOT NULL,
    receive_notifications boolean NOT NULL,
    is_ready boolean NOT NULL,
    is_active boolean NOT NULL
);
 &   DROP TABLE enterprise.profile_member;
    
   enterprise         heap    postgres    false    5            R           0    0    COLUMN profile_member.city_id    COMMENT     [   COMMENT ON COLUMN enterprise.profile_member.city_id IS 'City to which the player belongs';
       
   enterprise          postgres    false    210            �            1259    97088    profile_pair_player    TABLE     �   CREATE TABLE enterprise.profile_pair_player (
    profile_id character varying NOT NULL,
    level character varying(60),
    updated_by character varying NOT NULL,
    updated_date date NOT NULL,
    elo numeric(24,4)
);
 +   DROP TABLE enterprise.profile_pair_player;
    
   enterprise         heap    postgres    false    5            �            1259    97094    profile_referee    TABLE     �   CREATE TABLE enterprise.profile_referee (
    profile_id character varying NOT NULL,
    level character varying(60),
    updated_by character varying NOT NULL,
    updated_date date NOT NULL
);
 '   DROP TABLE enterprise.profile_referee;
    
   enterprise         heap    postgres    false    5            �            1259    97100    profile_single_player    TABLE     �   CREATE TABLE enterprise.profile_single_player (
    profile_id character varying NOT NULL,
    elo numeric(24,4),
    updated_by character varying NOT NULL,
    updated_date date NOT NULL,
    level character varying(60)
);
 -   DROP TABLE enterprise.profile_single_player;
    
   enterprise         heap    postgres    false    5            �            1259    97106    profile_team_player    TABLE     �   CREATE TABLE enterprise.profile_team_player (
    profile_id character varying NOT NULL,
    level character varying(60),
    amount_members integer,
    updated_by character varying NOT NULL,
    updated_date date NOT NULL,
    elo numeric(24,4)
);
 +   DROP TABLE enterprise.profile_team_player;
    
   enterprise         heap    postgres    false    5            �            1259    97112    profile_type    TABLE     2  CREATE TABLE enterprise.profile_type (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    description character varying(150) NOT NULL,
    created_by character varying(50) NOT NULL,
    created_date timestamp without time zone NOT NULL,
    by_default boolean,
    is_active boolean
);
 $   DROP TABLE enterprise.profile_type;
    
   enterprise         heap    postgres    false    5            �            1259    97115    profile_type_id_seq    SEQUENCE     �   CREATE SEQUENCE enterprise.profile_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE enterprise.profile_type_id_seq;
    
   enterprise          postgres    false    215    5            S           0    0    profile_type_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE enterprise.profile_type_id_seq OWNED BY enterprise.profile_type.id;
       
   enterprise          postgres    false    216            �            1259    97117    profile_users    TABLE     =  CREATE TABLE enterprise.profile_users (
    profile_id character varying NOT NULL,
    username character varying NOT NULL,
    is_principal boolean NOT NULL,
    created_by character varying NOT NULL,
    created_date date NOT NULL,
    is_confirmed boolean DEFAULT false,
    single_profile_id character varying
);
 %   DROP TABLE enterprise.profile_users;
    
   enterprise         heap    postgres    false    5            �            1259    97124    user_eventroles    TABLE     �   CREATE TABLE enterprise.user_eventroles (
    username character varying(50) NOT NULL,
    eventrol_id integer NOT NULL,
    created_by character varying NOT NULL,
    created_date timestamp without time zone NOT NULL
);
 '   DROP TABLE enterprise.user_eventroles;
    
   enterprise         heap    postgres    false    5            �            1259    97130    user_followers    TABLE     �   CREATE TABLE enterprise.user_followers (
    username character varying(50) NOT NULL,
    user_follow character varying(50) NOT NULL,
    created_date timestamp without time zone NOT NULL,
    is_active boolean NOT NULL
);
 &   DROP TABLE enterprise.user_followers;
    
   enterprise         heap    postgres    false    5            �            1259    97133    users    TABLE     �  CREATE TABLE enterprise.users (
    id character varying NOT NULL,
    username character varying(50) NOT NULL,
    first_name character varying(100) NOT NULL,
    last_name character varying(100),
    email character varying(50),
    phone character varying(12),
    password character varying(255) NOT NULL,
    is_active boolean NOT NULL,
    country_id integer,
    security_code character varying(5),
    sex character varying(1),
    birthdate date,
    alias character varying(30),
    job character varying(120),
    city_id integer,
    photo character varying(255),
    elo integer,
    receive_notifications boolean DEFAULT false
);
    DROP TABLE enterprise.users;
    
   enterprise         heap    postgres    false    5            T           0    0    COLUMN users.city_id    COMMENT     R   COMMENT ON COLUMN enterprise.users.city_id IS 'City to which the player belongs';
       
   enterprise          postgres    false    220            �            1259    97140    domino_boletus    TABLE     �  CREATE TABLE events.domino_boletus (
    id character varying NOT NULL,
    tourney_id character varying NOT NULL,
    round_id character varying NOT NULL,
    table_id character varying NOT NULL,
    is_valid boolean NOT NULL,
    status_id integer NOT NULL,
    can_update boolean,
    motive_closed character varying,
    motive_closed_description character varying,
    motive_not_valid character varying,
    motive_not_valid_description character varying
);
 "   DROP TABLE events.domino_boletus;
       events         heap    postgres    false    10            �            1259    97146    domino_boletus_data    TABLE     �  CREATE TABLE events.domino_boletus_data (
    id character varying NOT NULL,
    boletus_id character varying,
    data_number integer NOT NULL,
    win_pair_id character varying,
    win_by_points boolean NOT NULL,
    win_by_time boolean NOT NULL,
    number_points integer,
    start_date timestamp without time zone NOT NULL,
    end_date timestamp without time zone NOT NULL,
    duration double precision
);
 '   DROP TABLE events.domino_boletus_data;
       events         heap    postgres    false    10            �            1259    97152    domino_boletus_pairs    TABLE     �  CREATE TABLE events.domino_boletus_pairs (
    boletus_id character varying NOT NULL,
    pairs_id character varying NOT NULL,
    is_initiator boolean NOT NULL,
    is_winner boolean NOT NULL,
    positive_points integer,
    negative_points integer,
    start_date timestamp without time zone NOT NULL,
    end_date timestamp without time zone NOT NULL,
    duration double precision,
    penalty_points integer
);
 (   DROP TABLE events.domino_boletus_pairs;
       events         heap    postgres    false    10                       1259    98164    domino_boletus_penalties    TABLE     T  CREATE TABLE events.domino_boletus_penalties (
    id character varying NOT NULL,
    boletus_id character varying,
    pair_id character varying,
    player_id character varying,
    single_profile_id character varying,
    penalty_type character varying,
    penalty_amount integer,
    penalty_value integer,
    apply_points boolean
);
 ,   DROP TABLE events.domino_boletus_penalties;
       events         heap    postgres    false    10            �            1259    97158    domino_boletus_position    TABLE     �  CREATE TABLE events.domino_boletus_position (
    boletus_id character varying NOT NULL,
    position_id integer NOT NULL,
    single_profile_id character varying,
    scale_number integer,
    is_winner boolean,
    positive_points integer,
    negative_points integer,
    penalty_points integer,
    expelled boolean,
    pairs_id character varying,
    is_guilty_closure boolean
);
 +   DROP TABLE events.domino_boletus_position;
       events         heap    postgres    false    10            �            1259    97164    domino_categories    TABLE     ^  CREATE TABLE events.domino_categories (
    id character varying NOT NULL,
    tourney_id character varying NOT NULL,
    category_number character varying(100) NOT NULL,
    position_number integer NOT NULL,
    elo_min double precision NOT NULL,
    elo_max double precision NOT NULL,
    amount_players integer NOT NULL,
    by_default boolean
);
 %   DROP TABLE events.domino_categories;
       events         heap    postgres    false    10            �            1259    97170    domino_rounds    TABLE     �  CREATE TABLE events.domino_rounds (
    id character varying NOT NULL,
    tourney_id character varying NOT NULL,
    round_number integer NOT NULL,
    summary text,
    start_date timestamp without time zone NOT NULL,
    close_date timestamp without time zone NOT NULL,
    is_first boolean NOT NULL,
    is_last boolean NOT NULL,
    use_segmentation boolean NOT NULL,
    use_bonus boolean NOT NULL,
    amount_bonus_tables integer NOT NULL,
    amount_bonus_points integer NOT NULL,
    created_by character varying NOT NULL,
    created_date date NOT NULL,
    updated_by character varying,
    updated_date date NOT NULL,
    status_id integer NOT NULL,
    amount_tables integer DEFAULT 0,
    amount_players_playing integer DEFAULT 0,
    amount_players_waiting integer DEFAULT 0,
    amount_players_pause integer DEFAULT 0,
    amount_players_expelled integer DEFAULT 0,
    amount_categories integer DEFAULT 0
);
 !   DROP TABLE events.domino_rounds;
       events         heap    postgres    false    10            �            1259    97182    domino_rounds_pairs    TABLE     �  CREATE TABLE events.domino_rounds_pairs (
    id character varying NOT NULL,
    tourney_id character varying,
    round_id character varying NOT NULL,
    position_number integer NOT NULL,
    one_player_id character varying,
    two_player_id character varying,
    name character varying(100),
    profile_type character varying NOT NULL,
    player_id character varying,
    created_by character varying NOT NULL,
    created_date date NOT NULL,
    updated_by character varying NOT NULL,
    updated_date date NOT NULL,
    is_active boolean NOT NULL,
    scale_number_one_player integer,
    scale_number_two_player integer,
    scale_id_one_player character varying,
    scale_id_two_player character varying,
    games_won integer,
    games_lost integer,
    points_positive integer,
    points_negative integer,
    points_difference integer,
    score_expected double precision,
    score_obtained double precision,
    elo_pair double precision,
    elo_pair_opposing double precision,
    acumulated_games_played integer,
    k_value double precision,
    elo_current double precision,
    elo_at_end double precision,
    bonus_points double precision,
    elo_ra double precision,
    penalty_points double precision
);
 '   DROP TABLE events.domino_rounds_pairs;
       events         heap    postgres    false    10            �            1259    97188    domino_rounds_scale    TABLE     B  CREATE TABLE events.domino_rounds_scale (
    id character varying NOT NULL,
    tourney_id character varying NOT NULL,
    round_id character varying NOT NULL,
    round_number integer NOT NULL,
    position_number integer NOT NULL,
    player_id character varying,
    elo double precision,
    elo_variable double precision,
    games_played integer,
    games_won integer,
    games_lost integer,
    points_positive integer,
    points_negative integer,
    points_difference integer,
    is_active boolean NOT NULL,
    category_id character varying,
    score_expected double precision,
    score_obtained double precision,
    acumulated_games_played integer,
    k_value double precision,
    elo_at_end double precision,
    bonus_points double precision,
    elo_ra double precision,
    penalty_points double precision
);
 '   DROP TABLE events.domino_rounds_scale;
       events         heap    postgres    false    10            �            1259    97194    domino_tables    TABLE     �  CREATE TABLE events.domino_tables (
    id character varying NOT NULL,
    tourney_id character varying NOT NULL,
    table_number integer NOT NULL,
    is_smart boolean NOT NULL,
    amount_bonus integer NOT NULL,
    image text,
    is_active boolean NOT NULL,
    created_by character varying NOT NULL,
    created_date date NOT NULL,
    updated_by character varying,
    updated_date date NOT NULL
);
 !   DROP TABLE events.domino_tables;
       events         heap    postgres    false    10            �            1259    97200    domino_tables_files    TABLE     �   CREATE TABLE events.domino_tables_files (
    id character varying NOT NULL,
    table_id character varying NOT NULL,
    "position" integer NOT NULL,
    is_ready boolean NOT NULL
);
 '   DROP TABLE events.domino_tables_files;
       events         heap    postgres    false    10            �            1259    97206    events    TABLE     8  CREATE TABLE events.events (
    id character varying NOT NULL,
    name character varying(100) NOT NULL,
    start_date date NOT NULL,
    close_date date NOT NULL,
    registration_date date NOT NULL,
    registration_price double precision,
    city_id integer NOT NULL,
    main_location character varying(255),
    summary text,
    image text,
    status_id integer NOT NULL,
    created_by character varying NOT NULL,
    created_date date NOT NULL,
    updated_by character varying NOT NULL,
    updated_date date NOT NULL,
    profile_id character varying
);
    DROP TABLE events.events;
       events         heap    postgres    false    10            �            1259    97212    events_followers    TABLE     U  CREATE TABLE events.events_followers (
    id character varying NOT NULL,
    profile_id character varying,
    username character varying NOT NULL,
    element_type character varying(30) NOT NULL,
    element_id character varying,
    created_by character varying NOT NULL,
    created_date date NOT NULL,
    is_active boolean NOT NULL
);
 $   DROP TABLE events.events_followers;
       events         heap    postgres    false    10            �            1259    97218 	   gamerules    TABLE     �   CREATE TABLE events.gamerules (
    tourney_id character varying NOT NULL,
    amount_points integer,
    amount_time integer
);
    DROP TABLE events.gamerules;
       events         heap    postgres    false    10            �            1259    97224    invitations    TABLE     �  CREATE TABLE events.invitations (
    id character varying NOT NULL,
    tourney_id character varying NOT NULL,
    profile_id character varying NOT NULL,
    modality character varying(30) NOT NULL,
    status_name character varying NOT NULL,
    created_by character varying NOT NULL,
    created_date date NOT NULL,
    updated_by character varying,
    updated_date date NOT NULL
);
    DROP TABLE events.invitations;
       events         heap    postgres    false    10            �            1259    97230    players    TABLE     �  CREATE TABLE events.players (
    id character varying NOT NULL,
    tourney_id character varying NOT NULL,
    profile_id character varying NOT NULL,
    invitation_id character varying NOT NULL,
    created_by character varying NOT NULL,
    created_date date NOT NULL,
    updated_by character varying NOT NULL,
    updated_date date NOT NULL,
    elo double precision,
    level character varying(60),
    status_id integer NOT NULL
);
    DROP TABLE events.players;
       events         heap    postgres    false    10            �            1259    97236    players_users    TABLE     �  CREATE TABLE events.players_users (
    player_id character varying NOT NULL,
    profile_id character varying NOT NULL,
    level character varying(60),
    elo double precision,
    elo_current double precision,
    elo_at_end double precision,
    games_played integer,
    games_won integer,
    games_lost integer,
    points_positive integer,
    points_negative integer,
    points_difference integer,
    score_expected double precision,
    score_obtained double precision,
    k_value double precision,
    penalty_yellow integer,
    penalty_red integer,
    penalty_total integer,
    bonus_points double precision,
    category_id character varying,
    category_number integer,
    elo_ra double precision
);
 !   DROP TABLE events.players_users;
       events         heap    postgres    false    10            �            1259    97242    referees    TABLE     ~  CREATE TABLE events.referees (
    id character varying NOT NULL,
    tourney_id character varying NOT NULL,
    profile_id character varying NOT NULL,
    invitation_id character varying NOT NULL,
    created_by character varying NOT NULL,
    created_date date NOT NULL,
    updated_by character varying NOT NULL,
    updated_date date NOT NULL,
    status_id integer NOT NULL
);
    DROP TABLE events.referees;
       events         heap    postgres    false    10            �            1259    97248    sponsors    TABLE     t   CREATE TABLE events.sponsors (
    id integer NOT NULL,
    tourney_id character varying,
    name text NOT NULL
);
    DROP TABLE events.sponsors;
       events         heap    postgres    false    10            �            1259    97254    sponsors_id_seq    SEQUENCE     �   CREATE SEQUENCE events.sponsors_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE events.sponsors_id_seq;
       events          postgres    false    10    238            U           0    0    sponsors_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE events.sponsors_id_seq OWNED BY events.sponsors.id;
          events          postgres    false    239            �            1259    97256    tourney    TABLE     �  CREATE TABLE events.tourney (
    id character varying NOT NULL,
    event_id character varying NOT NULL,
    modality character varying(30) NOT NULL,
    name character varying(100),
    summary text,
    start_date date NOT NULL,
    close_date date,
    amount_tables integer NOT NULL,
    amount_smart_tables integer NOT NULL,
    amount_rounds integer NOT NULL,
    number_points_to_win integer NOT NULL,
    time_to_win integer NOT NULL,
    game_system character varying(120),
    lottery_type character varying(120),
    penalties_limit integer,
    image text,
    use_bonus boolean,
    use_segmentation boolean,
    amount_bonus_tables integer,
    amount_bonus_points integer,
    number_bonus_round integer,
    elo_min double precision,
    elo_max double precision,
    profile_id character varying NOT NULL,
    created_by character varying NOT NULL,
    created_date date NOT NULL,
    updated_date date NOT NULL,
    updated_by character varying NOT NULL,
    status_id integer NOT NULL,
    number_rounds integer,
    constant_increase_elo double precision,
    round_ordering_one character varying(120),
    round_ordering_two character varying(120),
    round_ordering_three character varying(120),
    round_ordering_four character varying(120),
    round_ordering_five character varying(120),
    event_ordering_one character varying(120),
    event_ordering_two character varying(120),
    event_ordering_three character varying(120),
    event_ordering_four character varying(120),
    event_ordering_five character varying(120),
    points_penalty_yellow integer DEFAULT 0,
    points_penalty_red integer DEFAULT 0,
    use_penalty boolean,
    amount_bonus_points_rounds integer,
    scope_tourney integer,
    level_tourney integer,
    round_ordering_dir_one character varying(5),
    round_ordering_dir_two character varying(5),
    round_ordering_dir_three character varying(5),
    round_ordering_dir_four character varying(5),
    round_ordering_dir_five character varying(5),
    event_ordering_dir_one character varying(5),
    event_ordering_dir_two character varying(5),
    event_ordering_dir_three character varying(5),
    event_ordering_dir_four character varying(5),
    event_ordering_dir_five character varying(5),
    points_for_absences integer
);
    DROP TABLE events.tourney;
       events         heap    postgres    false    10            �            1259    97264    trace_lottery_manual    TABLE       CREATE TABLE events.trace_lottery_manual (
    id character varying NOT NULL,
    tourney_id character varying,
    modality character varying(30) NOT NULL,
    position_number integer NOT NULL,
    player_id character varying NOT NULL,
    is_active boolean NOT NULL
);
 (   DROP TABLE events.trace_lottery_manual;
       events         heap    postgres    false    10            �            1259    97270    notifications    TABLE     �  CREATE TABLE notifications.notifications (
    id character varying NOT NULL,
    profile_id character varying NOT NULL,
    subject text,
    summary text,
    is_read boolean NOT NULL,
    created_by character varying NOT NULL,
    created_date timestamp without time zone NOT NULL,
    read_date timestamp without time zone NOT NULL,
    remove_date timestamp without time zone NOT NULL,
    is_active boolean NOT NULL
);
 (   DROP TABLE notifications.notifications;
       notifications         heap    postgres    false    12            �            1259    97276    comment_comments    TABLE       CREATE TABLE post.comment_comments (
    id character varying NOT NULL,
    comment_id character varying NOT NULL,
    summary text,
    created_by character varying NOT NULL,
    created_date timestamp without time zone NOT NULL,
    profile_id character varying
);
 "   DROP TABLE post.comment_comments;
       post         heap    postgres    false    9            �            1259    97282    comment_likes    TABLE     �   CREATE TABLE post.comment_likes (
    id character varying NOT NULL,
    comment_id character varying NOT NULL,
    created_by character varying NOT NULL,
    created_date timestamp without time zone NOT NULL,
    profile_id character varying
);
    DROP TABLE post.comment_likes;
       post         heap    postgres    false    9            �            1259    97288    post    TABLE     �  CREATE TABLE post.post (
    id character varying NOT NULL,
    summary text,
    created_by character varying NOT NULL,
    created_date timestamp without time zone NOT NULL,
    updated_by character varying,
    updated_date timestamp without time zone NOT NULL,
    is_active boolean NOT NULL,
    allow_comment boolean DEFAULT true NOT NULL,
    show_count_like boolean DEFAULT true NOT NULL,
    profile_id character varying
);
    DROP TABLE post.post;
       post         heap    postgres    false    9            �            1259    97296    post_comments    TABLE       CREATE TABLE post.post_comments (
    id character varying NOT NULL,
    post_id character varying NOT NULL,
    summary text,
    created_by character varying NOT NULL,
    created_date timestamp without time zone NOT NULL,
    profile_id character varying
);
    DROP TABLE post.post_comments;
       post         heap    postgres    false    9            �            1259    97302 
   post_files    TABLE     �   CREATE TABLE post.post_files (
    id character varying NOT NULL,
    post_id character varying NOT NULL,
    path text NOT NULL
);
    DROP TABLE post.post_files;
       post         heap    postgres    false    9            �            1259    97308 
   post_likes    TABLE     �   CREATE TABLE post.post_likes (
    id character varying NOT NULL,
    post_id character varying NOT NULL,
    created_by character varying NOT NULL,
    created_date timestamp without time zone NOT NULL,
    profile_id character varying
);
    DROP TABLE post.post_likes;
       post         heap    postgres    false    9            �            1259    97314    alembic_version    TABLE     X   CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);
 #   DROP TABLE public.alembic_version;
       public         heap    postgres    false            �            1259    97317    city    TABLE     �   CREATE TABLE resources.city (
    id integer NOT NULL,
    name character varying(120) NOT NULL,
    country_id integer,
    is_active boolean NOT NULL
);
    DROP TABLE resources.city;
    	   resources         heap    postgres    false    7            �            1259    97320    city_id_seq    SEQUENCE     �   CREATE SEQUENCE resources.city_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE resources.city_id_seq;
    	   resources          postgres    false    7    250            V           0    0    city_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE resources.city_id_seq OWNED BY resources.city.id;
       	   resources          postgres    false    251            �            1259    97322    country    TABLE     �   CREATE TABLE resources.country (
    id integer NOT NULL,
    name character varying(120) NOT NULL,
    is_active boolean NOT NULL
);
    DROP TABLE resources.country;
    	   resources         heap    postgres    false    7            �            1259    97325    country_id_seq    SEQUENCE     �   CREATE SEQUENCE resources.country_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE resources.country_id_seq;
    	   resources          postgres    false    7    252            W           0    0    country_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE resources.country_id_seq OWNED BY resources.country.id;
       	   resources          postgres    false    253            �            1259    97327    entities_status    TABLE       CREATE TABLE resources.entities_status (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    description character varying(100) NOT NULL,
    created_by character varying(50) NOT NULL,
    created_date timestamp without time zone NOT NULL
);
 &   DROP TABLE resources.entities_status;
    	   resources         heap    postgres    false    7            �            1259    97330    entities_status_id_seq    SEQUENCE     �   CREATE SEQUENCE resources.entities_status_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 0   DROP SEQUENCE resources.entities_status_id_seq;
    	   resources          postgres    false    7    254            X           0    0    entities_status_id_seq    SEQUENCE OWNED BY     W   ALTER SEQUENCE resources.entities_status_id_seq OWNED BY resources.entities_status.id;
       	   resources          postgres    false    255                        1259    97332    event_roles    TABLE        CREATE TABLE resources.event_roles (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    description character varying(100) NOT NULL,
    created_by character varying(50) NOT NULL,
    created_date timestamp without time zone NOT NULL
);
 "   DROP TABLE resources.event_roles;
    	   resources         heap    postgres    false    7                       1259    97335    event_roles_id_seq    SEQUENCE     �   CREATE SEQUENCE resources.event_roles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE resources.event_roles_id_seq;
    	   resources          postgres    false    7    256            Y           0    0    event_roles_id_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE resources.event_roles_id_seq OWNED BY resources.event_roles.id;
       	   resources          postgres    false    257                       1259    97337    events_levels    TABLE     �   CREATE TABLE resources.events_levels (
    id integer NOT NULL,
    level character varying(50) NOT NULL,
    description character varying(50) NOT NULL,
    value double precision NOT NULL
);
 $   DROP TABLE resources.events_levels;
    	   resources         heap    postgres    false    7                       1259    97340    events_levels_id_seq    SEQUENCE     �   CREATE SEQUENCE resources.events_levels_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE resources.events_levels_id_seq;
    	   resources          postgres    false    258    7            Z           0    0    events_levels_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE resources.events_levels_id_seq OWNED BY resources.events_levels.id;
       	   resources          postgres    false    259                       1259    97342    events_scopes    TABLE     �   CREATE TABLE resources.events_scopes (
    id integer NOT NULL,
    scope character varying(50) NOT NULL,
    description character varying(50) NOT NULL,
    value double precision NOT NULL
);
 $   DROP TABLE resources.events_scopes;
    	   resources         heap    postgres    false    7                       1259    97345    events_scopes_id_seq    SEQUENCE     �   CREATE SEQUENCE resources.events_scopes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE resources.events_scopes_id_seq;
    	   resources          postgres    false    260    7            [           0    0    events_scopes_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE resources.events_scopes_id_seq OWNED BY resources.events_scopes.id;
       	   resources          postgres    false    261                       1259    97347 	   ext_types    TABLE     �   CREATE TABLE resources.ext_types (
    id integer NOT NULL,
    ext_code character varying(10) NOT NULL,
    type_file character varying(10) NOT NULL,
    created_by character varying(50) NOT NULL,
    created_date timestamp without time zone NOT NULL
);
     DROP TABLE resources.ext_types;
    	   resources         heap    postgres    false    7                       1259    97350    ext_types_id_seq    SEQUENCE     �   CREATE SEQUENCE resources.ext_types_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE resources.ext_types_id_seq;
    	   resources          postgres    false    262    7            \           0    0    ext_types_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE resources.ext_types_id_seq OWNED BY resources.ext_types.id;
       	   resources          postgres    false    263                       1259    97352    jugadores_eeuu    TABLE       CREATE TABLE resources.jugadores_eeuu (
    id character varying(100) NOT NULL,
    nombre character varying(100),
    apellidos character varying(200),
    pais character varying(100),
    elo_inicial numeric(24,4),
    nivel character varying(100),
    sorteo integer
);
 %   DROP TABLE resources.jugadores_eeuu;
    	   resources         heap    postgres    false    7            	           1259    97358    jugadores_ind    TABLE     �  CREATE TABLE resources.jugadores_ind (
    id character varying(100) NOT NULL,
    nombre_completo character varying(100),
    nombre character varying(100),
    apellido_uno character varying(100),
    apellido_dos character varying(100),
    alias character varying(100),
    username character varying(100),
    provincia character varying(100),
    pais character varying(100),
    elo numeric(24,4),
    nivel character varying(100),
    sorteo integer
);
 $   DROP TABLE resources.jugadores_ind;
    	   resources         heap    postgres    false    7            
           1259    97364    packages    TABLE     \  CREATE TABLE resources.packages (
    id integer NOT NULL,
    name character varying(120) NOT NULL,
    price double precision,
    number_individual_tourney integer,
    number_pairs_tourney integer,
    number_team_tourney integer,
    is_active boolean NOT NULL,
    created_by character varying(50) NOT NULL,
    created_date date NOT NULL
);
    DROP TABLE resources.packages;
    	   resources         heap    postgres    false    7                       1259    97367    packages_id_seq    SEQUENCE     �   CREATE SEQUENCE resources.packages_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE resources.packages_id_seq;
    	   resources          postgres    false    7    266            ]           0    0    packages_id_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE resources.packages_id_seq OWNED BY resources.packages.id;
       	   resources          postgres    false    267                       1259    97369    player_categories    TABLE       CREATE TABLE resources.player_categories (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    value_k double precision NOT NULL,
    begin_elo double precision NOT NULL,
    end_elo double precision NOT NULL,
    width double precision NOT NULL,
    scope integer
);
 (   DROP TABLE resources.player_categories;
    	   resources         heap    postgres    false    7                       1259    97372    player_categories_id_seq    SEQUENCE     �   CREATE SEQUENCE resources.player_categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 2   DROP SEQUENCE resources.player_categories_id_seq;
    	   resources          postgres    false    268    7            ^           0    0    player_categories_id_seq    SEQUENCE OWNED BY     [   ALTER SEQUENCE resources.player_categories_id_seq OWNED BY resources.player_categories.id;
       	   resources          postgres    false    269            �           2604    97374    profile_type id    DEFAULT     z   ALTER TABLE ONLY enterprise.profile_type ALTER COLUMN id SET DEFAULT nextval('enterprise.profile_type_id_seq'::regclass);
 B   ALTER TABLE enterprise.profile_type ALTER COLUMN id DROP DEFAULT;
    
   enterprise          postgres    false    216    215            �           2604    97375    sponsors id    DEFAULT     j   ALTER TABLE ONLY events.sponsors ALTER COLUMN id SET DEFAULT nextval('events.sponsors_id_seq'::regclass);
 :   ALTER TABLE events.sponsors ALTER COLUMN id DROP DEFAULT;
       events          postgres    false    239    238            �           2604    97376    city id    DEFAULT     h   ALTER TABLE ONLY resources.city ALTER COLUMN id SET DEFAULT nextval('resources.city_id_seq'::regclass);
 9   ALTER TABLE resources.city ALTER COLUMN id DROP DEFAULT;
    	   resources          postgres    false    251    250            �           2604    97377 
   country id    DEFAULT     n   ALTER TABLE ONLY resources.country ALTER COLUMN id SET DEFAULT nextval('resources.country_id_seq'::regclass);
 <   ALTER TABLE resources.country ALTER COLUMN id DROP DEFAULT;
    	   resources          postgres    false    253    252            �           2604    97378    entities_status id    DEFAULT     ~   ALTER TABLE ONLY resources.entities_status ALTER COLUMN id SET DEFAULT nextval('resources.entities_status_id_seq'::regclass);
 D   ALTER TABLE resources.entities_status ALTER COLUMN id DROP DEFAULT;
    	   resources          postgres    false    255    254            �           2604    97379    event_roles id    DEFAULT     v   ALTER TABLE ONLY resources.event_roles ALTER COLUMN id SET DEFAULT nextval('resources.event_roles_id_seq'::regclass);
 @   ALTER TABLE resources.event_roles ALTER COLUMN id DROP DEFAULT;
    	   resources          postgres    false    257    256            �           2604    97380    events_levels id    DEFAULT     z   ALTER TABLE ONLY resources.events_levels ALTER COLUMN id SET DEFAULT nextval('resources.events_levels_id_seq'::regclass);
 B   ALTER TABLE resources.events_levels ALTER COLUMN id DROP DEFAULT;
    	   resources          postgres    false    259    258            �           2604    97381    events_scopes id    DEFAULT     z   ALTER TABLE ONLY resources.events_scopes ALTER COLUMN id SET DEFAULT nextval('resources.events_scopes_id_seq'::regclass);
 B   ALTER TABLE resources.events_scopes ALTER COLUMN id DROP DEFAULT;
    	   resources          postgres    false    261    260            �           2604    97382    ext_types id    DEFAULT     r   ALTER TABLE ONLY resources.ext_types ALTER COLUMN id SET DEFAULT nextval('resources.ext_types_id_seq'::regclass);
 >   ALTER TABLE resources.ext_types ALTER COLUMN id DROP DEFAULT;
    	   resources          postgres    false    263    262            �           2604    97383    packages id    DEFAULT     p   ALTER TABLE ONLY resources.packages ALTER COLUMN id SET DEFAULT nextval('resources.packages_id_seq'::regclass);
 =   ALTER TABLE resources.packages ALTER COLUMN id DROP DEFAULT;
    	   resources          postgres    false    267    266            �           2604    97384    player_categories id    DEFAULT     �   ALTER TABLE ONLY resources.player_categories ALTER COLUMN id SET DEFAULT nextval('resources.player_categories_id_seq'::regclass);
 F   ALTER TABLE resources.player_categories ALTER COLUMN id DROP DEFAULT;
    	   resources          postgres    false    269    268            
          0    97064    profile_default_user 
   TABLE DATA           }   COPY enterprise.profile_default_user (profile_id, sex, birthdate, alias, job, city_id, updated_by, updated_date) FROM stdin;
 
   enterprise          postgres    false    207   �                0    97070    profile_event_admon 
   TABLE DATA           W   COPY enterprise.profile_event_admon (profile_id, updated_by, updated_date) FROM stdin;
 
   enterprise          postgres    false    208   �                0    97076    profile_followers 
   TABLE DATA           �   COPY enterprise.profile_followers (profile_id, username, profile_follow_id, username_follow, created_by, created_date, is_active) FROM stdin;
 
   enterprise          postgres    false    209   �                0    97082    profile_member 
   TABLE DATA           �   COPY enterprise.profile_member (id, profile_type, name, email, photo, city_id, created_by, created_date, updated_by, updated_date, receive_notifications, is_ready, is_active) FROM stdin;
 
   enterprise          postgres    false    210   �                0    97088    profile_pair_player 
   TABLE DATA           c   COPY enterprise.profile_pair_player (profile_id, level, updated_by, updated_date, elo) FROM stdin;
 
   enterprise          postgres    false    211                   0    97094    profile_referee 
   TABLE DATA           Z   COPY enterprise.profile_referee (profile_id, level, updated_by, updated_date) FROM stdin;
 
   enterprise          postgres    false    212   1                0    97100    profile_single_player 
   TABLE DATA           e   COPY enterprise.profile_single_player (profile_id, elo, updated_by, updated_date, level) FROM stdin;
 
   enterprise          postgres    false    213   N                0    97106    profile_team_player 
   TABLE DATA           s   COPY enterprise.profile_team_player (profile_id, level, amount_members, updated_by, updated_date, elo) FROM stdin;
 
   enterprise          postgres    false    214   k                0    97112    profile_type 
   TABLE DATA           r   COPY enterprise.profile_type (id, name, description, created_by, created_date, by_default, is_active) FROM stdin;
 
   enterprise          postgres    false    215   �                0    97117    profile_users 
   TABLE DATA           �   COPY enterprise.profile_users (profile_id, username, is_principal, created_by, created_date, is_confirmed, single_profile_id) FROM stdin;
 
   enterprise          postgres    false    217   |                0    97124    user_eventroles 
   TABLE DATA           ^   COPY enterprise.user_eventroles (username, eventrol_id, created_by, created_date) FROM stdin;
 
   enterprise          postgres    false    218   �                0    97130    user_followers 
   TABLE DATA           \   COPY enterprise.user_followers (username, user_follow, created_date, is_active) FROM stdin;
 
   enterprise          postgres    false    219   �                0    97133    users 
   TABLE DATA           �   COPY enterprise.users (id, username, first_name, last_name, email, phone, password, is_active, country_id, security_code, sex, birthdate, alias, job, city_id, photo, elo, receive_notifications) FROM stdin;
 
   enterprise          postgres    false    220   �                0    97140    domino_boletus 
   TABLE DATA           �   COPY events.domino_boletus (id, tourney_id, round_id, table_id, is_valid, status_id, can_update, motive_closed, motive_closed_description, motive_not_valid, motive_not_valid_description) FROM stdin;
    events          postgres    false    221   �                0    97146    domino_boletus_data 
   TABLE DATA           �   COPY events.domino_boletus_data (id, boletus_id, data_number, win_pair_id, win_by_points, win_by_time, number_points, start_date, end_date, duration) FROM stdin;
    events          postgres    false    222                   0    97152    domino_boletus_pairs 
   TABLE DATA           �   COPY events.domino_boletus_pairs (boletus_id, pairs_id, is_initiator, is_winner, positive_points, negative_points, start_date, end_date, duration, penalty_points) FROM stdin;
    events          postgres    false    223   *      I          0    98164    domino_boletus_penalties 
   TABLE DATA           �   COPY events.domino_boletus_penalties (id, boletus_id, pair_id, player_id, single_profile_id, penalty_type, penalty_amount, penalty_value, apply_points) FROM stdin;
    events          postgres    false    270   G                0    97158    domino_boletus_position 
   TABLE DATA           �   COPY events.domino_boletus_position (boletus_id, position_id, single_profile_id, scale_number, is_winner, positive_points, negative_points, penalty_points, expelled, pairs_id, is_guilty_closure) FROM stdin;
    events          postgres    false    224   d                0    97164    domino_categories 
   TABLE DATA           �   COPY events.domino_categories (id, tourney_id, category_number, position_number, elo_min, elo_max, amount_players, by_default) FROM stdin;
    events          postgres    false    225   �                0    97170    domino_rounds 
   TABLE DATA           �  COPY events.domino_rounds (id, tourney_id, round_number, summary, start_date, close_date, is_first, is_last, use_segmentation, use_bonus, amount_bonus_tables, amount_bonus_points, created_by, created_date, updated_by, updated_date, status_id, amount_tables, amount_players_playing, amount_players_waiting, amount_players_pause, amount_players_expelled, amount_categories) FROM stdin;
    events          postgres    false    226   �                0    97182    domino_rounds_pairs 
   TABLE DATA             COPY events.domino_rounds_pairs (id, tourney_id, round_id, position_number, one_player_id, two_player_id, name, profile_type, player_id, created_by, created_date, updated_by, updated_date, is_active, scale_number_one_player, scale_number_two_player, scale_id_one_player, scale_id_two_player, games_won, games_lost, points_positive, points_negative, points_difference, score_expected, score_obtained, elo_pair, elo_pair_opposing, acumulated_games_played, k_value, elo_current, elo_at_end, bonus_points, elo_ra, penalty_points) FROM stdin;
    events          postgres    false    227   �                0    97188    domino_rounds_scale 
   TABLE DATA           j  COPY events.domino_rounds_scale (id, tourney_id, round_id, round_number, position_number, player_id, elo, elo_variable, games_played, games_won, games_lost, points_positive, points_negative, points_difference, is_active, category_id, score_expected, score_obtained, acumulated_games_played, k_value, elo_at_end, bonus_points, elo_ra, penalty_points) FROM stdin;
    events          postgres    false    228   �                 0    97194    domino_tables 
   TABLE DATA           �   COPY events.domino_tables (id, tourney_id, table_number, is_smart, amount_bonus, image, is_active, created_by, created_date, updated_by, updated_date) FROM stdin;
    events          postgres    false    229   �      !          0    97200    domino_tables_files 
   TABLE DATA           Q   COPY events.domino_tables_files (id, table_id, "position", is_ready) FROM stdin;
    events          postgres    false    230         "          0    97206    events 
   TABLE DATA           �   COPY events.events (id, name, start_date, close_date, registration_date, registration_price, city_id, main_location, summary, image, status_id, created_by, created_date, updated_by, updated_date, profile_id) FROM stdin;
    events          postgres    false    231   /      #          0    97212    events_followers 
   TABLE DATA           �   COPY events.events_followers (id, profile_id, username, element_type, element_id, created_by, created_date, is_active) FROM stdin;
    events          postgres    false    232   L      $          0    97218 	   gamerules 
   TABLE DATA           K   COPY events.gamerules (tourney_id, amount_points, amount_time) FROM stdin;
    events          postgres    false    233   i      %          0    97224    invitations 
   TABLE DATA           �   COPY events.invitations (id, tourney_id, profile_id, modality, status_name, created_by, created_date, updated_by, updated_date) FROM stdin;
    events          postgres    false    234   �      &          0    97230    players 
   TABLE DATA           �   COPY events.players (id, tourney_id, profile_id, invitation_id, created_by, created_date, updated_by, updated_date, elo, level, status_id) FROM stdin;
    events          postgres    false    235   �      '          0    97236    players_users 
   TABLE DATA           F  COPY events.players_users (player_id, profile_id, level, elo, elo_current, elo_at_end, games_played, games_won, games_lost, points_positive, points_negative, points_difference, score_expected, score_obtained, k_value, penalty_yellow, penalty_red, penalty_total, bonus_points, category_id, category_number, elo_ra) FROM stdin;
    events          postgres    false    236   �      (          0    97242    referees 
   TABLE DATA           �   COPY events.referees (id, tourney_id, profile_id, invitation_id, created_by, created_date, updated_by, updated_date, status_id) FROM stdin;
    events          postgres    false    237   �      )          0    97248    sponsors 
   TABLE DATA           8   COPY events.sponsors (id, tourney_id, name) FROM stdin;
    events          postgres    false    238   �      +          0    97256    tourney 
   TABLE DATA             COPY events.tourney (id, event_id, modality, name, summary, start_date, close_date, amount_tables, amount_smart_tables, amount_rounds, number_points_to_win, time_to_win, game_system, lottery_type, penalties_limit, image, use_bonus, use_segmentation, amount_bonus_tables, amount_bonus_points, number_bonus_round, elo_min, elo_max, profile_id, created_by, created_date, updated_date, updated_by, status_id, number_rounds, constant_increase_elo, round_ordering_one, round_ordering_two, round_ordering_three, round_ordering_four, round_ordering_five, event_ordering_one, event_ordering_two, event_ordering_three, event_ordering_four, event_ordering_five, points_penalty_yellow, points_penalty_red, use_penalty, amount_bonus_points_rounds, scope_tourney, level_tourney, round_ordering_dir_one, round_ordering_dir_two, round_ordering_dir_three, round_ordering_dir_four, round_ordering_dir_five, event_ordering_dir_one, event_ordering_dir_two, event_ordering_dir_three, event_ordering_dir_four, event_ordering_dir_five, points_for_absences) FROM stdin;
    events          postgres    false    240         ,          0    97264    trace_lottery_manual 
   TABLE DATA           o   COPY events.trace_lottery_manual (id, tourney_id, modality, position_number, player_id, is_active) FROM stdin;
    events          postgres    false    241   4      -          0    97270    notifications 
   TABLE DATA           �   COPY notifications.notifications (id, profile_id, subject, summary, is_read, created_by, created_date, read_date, remove_date, is_active) FROM stdin;
    notifications          postgres    false    242   Q      .          0    97276    comment_comments 
   TABLE DATA           g   COPY post.comment_comments (id, comment_id, summary, created_by, created_date, profile_id) FROM stdin;
    post          postgres    false    243   n      /          0    97282    comment_likes 
   TABLE DATA           [   COPY post.comment_likes (id, comment_id, created_by, created_date, profile_id) FROM stdin;
    post          postgres    false    244   �      0          0    97288    post 
   TABLE DATA           �   COPY post.post (id, summary, created_by, created_date, updated_by, updated_date, is_active, allow_comment, show_count_like, profile_id) FROM stdin;
    post          postgres    false    245   �      1          0    97296    post_comments 
   TABLE DATA           a   COPY post.post_comments (id, post_id, summary, created_by, created_date, profile_id) FROM stdin;
    post          postgres    false    246   �      2          0    97302 
   post_files 
   TABLE DATA           5   COPY post.post_files (id, post_id, path) FROM stdin;
    post          postgres    false    247   �      3          0    97308 
   post_likes 
   TABLE DATA           U   COPY post.post_likes (id, post_id, created_by, created_date, profile_id) FROM stdin;
    post          postgres    false    248   �      4          0    97314    alembic_version 
   TABLE DATA           6   COPY public.alembic_version (version_num) FROM stdin;
    public          postgres    false    249         5          0    97317    city 
   TABLE DATA           B   COPY resources.city (id, name, country_id, is_active) FROM stdin;
 	   resources          postgres    false    250   F      7          0    97322    country 
   TABLE DATA           9   COPY resources.country (id, name, is_active) FROM stdin;
 	   resources          postgres    false    252   7	      9          0    97327    entities_status 
   TABLE DATA           ]   COPY resources.entities_status (id, name, description, created_by, created_date) FROM stdin;
 	   resources          postgres    false    254   �	      ;          0    97332    event_roles 
   TABLE DATA           Y   COPY resources.event_roles (id, name, description, created_by, created_date) FROM stdin;
 	   resources          postgres    false    256   �
      =          0    97337    events_levels 
   TABLE DATA           I   COPY resources.events_levels (id, level, description, value) FROM stdin;
 	   resources          postgres    false    258   c      ?          0    97342    events_scopes 
   TABLE DATA           I   COPY resources.events_scopes (id, scope, description, value) FROM stdin;
 	   resources          postgres    false    260   �      A          0    97347 	   ext_types 
   TABLE DATA           Y   COPY resources.ext_types (id, ext_code, type_file, created_by, created_date) FROM stdin;
 	   resources          postgres    false    262   �      C          0    97352    jugadores_eeuu 
   TABLE DATA           d   COPY resources.jugadores_eeuu (id, nombre, apellidos, pais, elo_inicial, nivel, sorteo) FROM stdin;
 	   resources          postgres    false    264   r      D          0    97358    jugadores_ind 
   TABLE DATA           �   COPY resources.jugadores_ind (id, nombre_completo, nombre, apellido_uno, apellido_dos, alias, username, provincia, pais, elo, nivel, sorteo) FROM stdin;
 	   resources          postgres    false    265   �      E          0    97364    packages 
   TABLE DATA           �   COPY resources.packages (id, name, price, number_individual_tourney, number_pairs_tourney, number_team_tourney, is_active, created_by, created_date) FROM stdin;
 	   resources          postgres    false    266   �      G          0    97369    player_categories 
   TABLE DATA           c   COPY resources.player_categories (id, name, value_k, begin_elo, end_elo, width, scope) FROM stdin;
 	   resources          postgres    false    268         _           0    0    profile_type_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('enterprise.profile_type_id_seq', 6, true);
       
   enterprise          postgres    false    216            `           0    0    sponsors_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('events.sponsors_id_seq', 1, false);
          events          postgres    false    239            a           0    0    city_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('resources.city_id_seq', 80, true);
       	   resources          postgres    false    251            b           0    0    country_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('resources.country_id_seq', 70, true);
       	   resources          postgres    false    253            c           0    0    entities_status_id_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('resources.entities_status_id_seq', 7, true);
       	   resources          postgres    false    255            d           0    0    event_roles_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('resources.event_roles_id_seq', 5, true);
       	   resources          postgres    false    257            e           0    0    events_levels_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('resources.events_levels_id_seq', 3, true);
       	   resources          postgres    false    259            f           0    0    events_scopes_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('resources.events_scopes_id_seq', 3, true);
       	   resources          postgres    false    261            g           0    0    ext_types_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('resources.ext_types_id_seq', 15, true);
       	   resources          postgres    false    263            h           0    0    packages_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('resources.packages_id_seq', 2, true);
       	   resources          postgres    false    267            i           0    0    player_categories_id_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('resources.player_categories_id_seq', 7, true);
       	   resources          postgres    false    269            �           2606    97386 .   profile_default_user profile_default_user_pkey 
   CONSTRAINT     x   ALTER TABLE ONLY enterprise.profile_default_user
    ADD CONSTRAINT profile_default_user_pkey PRIMARY KEY (profile_id);
 \   ALTER TABLE ONLY enterprise.profile_default_user DROP CONSTRAINT profile_default_user_pkey;
    
   enterprise            postgres    false    207            �           2606    97388 ,   profile_event_admon profile_event_admon_pkey 
   CONSTRAINT     v   ALTER TABLE ONLY enterprise.profile_event_admon
    ADD CONSTRAINT profile_event_admon_pkey PRIMARY KEY (profile_id);
 Z   ALTER TABLE ONLY enterprise.profile_event_admon DROP CONSTRAINT profile_event_admon_pkey;
    
   enterprise            postgres    false    208            �           2606    97390 (   profile_followers profile_followers_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY enterprise.profile_followers
    ADD CONSTRAINT profile_followers_pkey PRIMARY KEY (profile_id, profile_follow_id);
 V   ALTER TABLE ONLY enterprise.profile_followers DROP CONSTRAINT profile_followers_pkey;
    
   enterprise            postgres    false    209    209            �           2606    97392 "   profile_member profile_member_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY enterprise.profile_member
    ADD CONSTRAINT profile_member_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY enterprise.profile_member DROP CONSTRAINT profile_member_pkey;
    
   enterprise            postgres    false    210            �           2606    97394 ,   profile_pair_player profile_pair_player_pkey 
   CONSTRAINT     v   ALTER TABLE ONLY enterprise.profile_pair_player
    ADD CONSTRAINT profile_pair_player_pkey PRIMARY KEY (profile_id);
 Z   ALTER TABLE ONLY enterprise.profile_pair_player DROP CONSTRAINT profile_pair_player_pkey;
    
   enterprise            postgres    false    211            �           2606    97396 $   profile_referee profile_referee_pkey 
   CONSTRAINT     n   ALTER TABLE ONLY enterprise.profile_referee
    ADD CONSTRAINT profile_referee_pkey PRIMARY KEY (profile_id);
 R   ALTER TABLE ONLY enterprise.profile_referee DROP CONSTRAINT profile_referee_pkey;
    
   enterprise            postgres    false    212            �           2606    97398 0   profile_single_player profile_single_player_pkey 
   CONSTRAINT     z   ALTER TABLE ONLY enterprise.profile_single_player
    ADD CONSTRAINT profile_single_player_pkey PRIMARY KEY (profile_id);
 ^   ALTER TABLE ONLY enterprise.profile_single_player DROP CONSTRAINT profile_single_player_pkey;
    
   enterprise            postgres    false    213            �           2606    97400 ,   profile_team_player profile_team_player_pkey 
   CONSTRAINT     v   ALTER TABLE ONLY enterprise.profile_team_player
    ADD CONSTRAINT profile_team_player_pkey PRIMARY KEY (profile_id);
 Z   ALTER TABLE ONLY enterprise.profile_team_player DROP CONSTRAINT profile_team_player_pkey;
    
   enterprise            postgres    false    214            �           2606    97402 "   profile_type profile_type_name_key 
   CONSTRAINT     a   ALTER TABLE ONLY enterprise.profile_type
    ADD CONSTRAINT profile_type_name_key UNIQUE (name);
 P   ALTER TABLE ONLY enterprise.profile_type DROP CONSTRAINT profile_type_name_key;
    
   enterprise            postgres    false    215            �           2606    97404    profile_type profile_type_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY enterprise.profile_type
    ADD CONSTRAINT profile_type_pkey PRIMARY KEY (id);
 L   ALTER TABLE ONLY enterprise.profile_type DROP CONSTRAINT profile_type_pkey;
    
   enterprise            postgres    false    215            �           2606    97406     profile_users profile_users_pkey 
   CONSTRAINT     t   ALTER TABLE ONLY enterprise.profile_users
    ADD CONSTRAINT profile_users_pkey PRIMARY KEY (profile_id, username);
 N   ALTER TABLE ONLY enterprise.profile_users DROP CONSTRAINT profile_users_pkey;
    
   enterprise            postgres    false    217    217            �           2606    97408 $   user_eventroles user_eventroles_pkey 
   CONSTRAINT     y   ALTER TABLE ONLY enterprise.user_eventroles
    ADD CONSTRAINT user_eventroles_pkey PRIMARY KEY (username, eventrol_id);
 R   ALTER TABLE ONLY enterprise.user_eventroles DROP CONSTRAINT user_eventroles_pkey;
    
   enterprise            postgres    false    218    218            �           2606    97410 "   user_followers user_followers_pkey 
   CONSTRAINT     w   ALTER TABLE ONLY enterprise.user_followers
    ADD CONSTRAINT user_followers_pkey PRIMARY KEY (username, user_follow);
 P   ALTER TABLE ONLY enterprise.user_followers DROP CONSTRAINT user_followers_pkey;
    
   enterprise            postgres    false    219    219            �           2606    97412    users users_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY enterprise.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY enterprise.users DROP CONSTRAINT users_pkey;
    
   enterprise            postgres    false    220            �           2606    97414    users users_username_key 
   CONSTRAINT     [   ALTER TABLE ONLY enterprise.users
    ADD CONSTRAINT users_username_key UNIQUE (username);
 F   ALTER TABLE ONLY enterprise.users DROP CONSTRAINT users_username_key;
    
   enterprise            postgres    false    220            �           2606    97416 ,   domino_boletus_data domino_boletus_data_pkey 
   CONSTRAINT     j   ALTER TABLE ONLY events.domino_boletus_data
    ADD CONSTRAINT domino_boletus_data_pkey PRIMARY KEY (id);
 V   ALTER TABLE ONLY events.domino_boletus_data DROP CONSTRAINT domino_boletus_data_pkey;
       events            postgres    false    222            �           2606    97418 .   domino_boletus_pairs domino_boletus_pairs_pkey 
   CONSTRAINT     ~   ALTER TABLE ONLY events.domino_boletus_pairs
    ADD CONSTRAINT domino_boletus_pairs_pkey PRIMARY KEY (boletus_id, pairs_id);
 X   ALTER TABLE ONLY events.domino_boletus_pairs DROP CONSTRAINT domino_boletus_pairs_pkey;
       events            postgres    false    223    223                       2606    98171 6   domino_boletus_penalties domino_boletus_penalties_pkey 
   CONSTRAINT     t   ALTER TABLE ONLY events.domino_boletus_penalties
    ADD CONSTRAINT domino_boletus_penalties_pkey PRIMARY KEY (id);
 `   ALTER TABLE ONLY events.domino_boletus_penalties DROP CONSTRAINT domino_boletus_penalties_pkey;
       events            postgres    false    270            �           2606    97420 "   domino_boletus domino_boletus_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY events.domino_boletus
    ADD CONSTRAINT domino_boletus_pkey PRIMARY KEY (id);
 L   ALTER TABLE ONLY events.domino_boletus DROP CONSTRAINT domino_boletus_pkey;
       events            postgres    false    221            �           2606    97422 4   domino_boletus_position domino_boletus_position_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY events.domino_boletus_position
    ADD CONSTRAINT domino_boletus_position_pkey PRIMARY KEY (boletus_id, position_id);
 ^   ALTER TABLE ONLY events.domino_boletus_position DROP CONSTRAINT domino_boletus_position_pkey;
       events            postgres    false    224    224            �           2606    97424 (   domino_categories domino_categories_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY events.domino_categories
    ADD CONSTRAINT domino_categories_pkey PRIMARY KEY (id);
 R   ALTER TABLE ONLY events.domino_categories DROP CONSTRAINT domino_categories_pkey;
       events            postgres    false    225            �           2606    97426 ,   domino_rounds_pairs domino_rounds_pairs_pkey 
   CONSTRAINT     j   ALTER TABLE ONLY events.domino_rounds_pairs
    ADD CONSTRAINT domino_rounds_pairs_pkey PRIMARY KEY (id);
 V   ALTER TABLE ONLY events.domino_rounds_pairs DROP CONSTRAINT domino_rounds_pairs_pkey;
       events            postgres    false    227            �           2606    97428     domino_rounds domino_rounds_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY events.domino_rounds
    ADD CONSTRAINT domino_rounds_pkey PRIMARY KEY (id);
 J   ALTER TABLE ONLY events.domino_rounds DROP CONSTRAINT domino_rounds_pkey;
       events            postgres    false    226            �           2606    97430 ,   domino_rounds_scale domino_rounds_scale_pkey 
   CONSTRAINT     j   ALTER TABLE ONLY events.domino_rounds_scale
    ADD CONSTRAINT domino_rounds_scale_pkey PRIMARY KEY (id);
 V   ALTER TABLE ONLY events.domino_rounds_scale DROP CONSTRAINT domino_rounds_scale_pkey;
       events            postgres    false    228            �           2606    97432 ,   domino_tables_files domino_tables_files_pkey 
   CONSTRAINT     j   ALTER TABLE ONLY events.domino_tables_files
    ADD CONSTRAINT domino_tables_files_pkey PRIMARY KEY (id);
 V   ALTER TABLE ONLY events.domino_tables_files DROP CONSTRAINT domino_tables_files_pkey;
       events            postgres    false    230            �           2606    97434     domino_tables domino_tables_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY events.domino_tables
    ADD CONSTRAINT domino_tables_pkey PRIMARY KEY (id);
 J   ALTER TABLE ONLY events.domino_tables DROP CONSTRAINT domino_tables_pkey;
       events            postgres    false    229            �           2606    97436 &   events_followers events_followers_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY events.events_followers
    ADD CONSTRAINT events_followers_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY events.events_followers DROP CONSTRAINT events_followers_pkey;
       events            postgres    false    232            �           2606    97438 0   events_followers events_followers_profile_id_key 
   CONSTRAINT     q   ALTER TABLE ONLY events.events_followers
    ADD CONSTRAINT events_followers_profile_id_key UNIQUE (profile_id);
 Z   ALTER TABLE ONLY events.events_followers DROP CONSTRAINT events_followers_profile_id_key;
       events            postgres    false    232            �           2606    97440    events events_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY events.events
    ADD CONSTRAINT events_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY events.events DROP CONSTRAINT events_pkey;
       events            postgres    false    231            �           2606    97442    gamerules gamerules_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY events.gamerules
    ADD CONSTRAINT gamerules_pkey PRIMARY KEY (tourney_id);
 B   ALTER TABLE ONLY events.gamerules DROP CONSTRAINT gamerules_pkey;
       events            postgres    false    233            �           2606    97444    invitations invitations_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY events.invitations
    ADD CONSTRAINT invitations_pkey PRIMARY KEY (id);
 F   ALTER TABLE ONLY events.invitations DROP CONSTRAINT invitations_pkey;
       events            postgres    false    234            �           2606    97446    players players_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY events.players
    ADD CONSTRAINT players_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY events.players DROP CONSTRAINT players_pkey;
       events            postgres    false    235            �           2606    97448    players_users players_user_pkey 
   CONSTRAINT     p   ALTER TABLE ONLY events.players_users
    ADD CONSTRAINT players_user_pkey PRIMARY KEY (player_id, profile_id);
 I   ALTER TABLE ONLY events.players_users DROP CONSTRAINT players_user_pkey;
       events            postgres    false    236    236            �           2606    97450    referees referees_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY events.referees
    ADD CONSTRAINT referees_pkey PRIMARY KEY (id, tourney_id);
 @   ALTER TABLE ONLY events.referees DROP CONSTRAINT referees_pkey;
       events            postgres    false    237    237            �           2606    97452    sponsors sponsors_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY events.sponsors
    ADD CONSTRAINT sponsors_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY events.sponsors DROP CONSTRAINT sponsors_pkey;
       events            postgres    false    238            �           2606    97454    tourney tourney_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY events.tourney
    ADD CONSTRAINT tourney_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY events.tourney DROP CONSTRAINT tourney_pkey;
       events            postgres    false    240            �           2606    97456 .   trace_lottery_manual trace_lottery_manual_pkey 
   CONSTRAINT     l   ALTER TABLE ONLY events.trace_lottery_manual
    ADD CONSTRAINT trace_lottery_manual_pkey PRIMARY KEY (id);
 X   ALTER TABLE ONLY events.trace_lottery_manual DROP CONSTRAINT trace_lottery_manual_pkey;
       events            postgres    false    241            �           2606    97458     notifications notifications_pkey 
   CONSTRAINT     e   ALTER TABLE ONLY notifications.notifications
    ADD CONSTRAINT notifications_pkey PRIMARY KEY (id);
 Q   ALTER TABLE ONLY notifications.notifications DROP CONSTRAINT notifications_pkey;
       notifications            postgres    false    242            �           2606    97460 &   comment_comments comment_comments_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY post.comment_comments
    ADD CONSTRAINT comment_comments_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY post.comment_comments DROP CONSTRAINT comment_comments_pkey;
       post            postgres    false    243            �           2606    97462     comment_likes comment_likes_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY post.comment_likes
    ADD CONSTRAINT comment_likes_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY post.comment_likes DROP CONSTRAINT comment_likes_pkey;
       post            postgres    false    244            �           2606    97464     post_comments post_comments_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY post.post_comments
    ADD CONSTRAINT post_comments_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY post.post_comments DROP CONSTRAINT post_comments_pkey;
       post            postgres    false    246            �           2606    97466    post_files post_files_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY post.post_files
    ADD CONSTRAINT post_files_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY post.post_files DROP CONSTRAINT post_files_pkey;
       post            postgres    false    247            �           2606    97468    post_likes post_likes_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY post.post_likes
    ADD CONSTRAINT post_likes_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY post.post_likes DROP CONSTRAINT post_likes_pkey;
       post            postgres    false    248            �           2606    97470    post post_pkey 
   CONSTRAINT     J   ALTER TABLE ONLY post.post
    ADD CONSTRAINT post_pkey PRIMARY KEY (id);
 6   ALTER TABLE ONLY post.post DROP CONSTRAINT post_pkey;
       post            postgres    false    245            �           2606    97472 #   alembic_version alembic_version_pkc 
   CONSTRAINT     j   ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);
 M   ALTER TABLE ONLY public.alembic_version DROP CONSTRAINT alembic_version_pkc;
       public            postgres    false    249            �           2606    97474    city city_pkey 
   CONSTRAINT     O   ALTER TABLE ONLY resources.city
    ADD CONSTRAINT city_pkey PRIMARY KEY (id);
 ;   ALTER TABLE ONLY resources.city DROP CONSTRAINT city_pkey;
    	   resources            postgres    false    250            �           2606    97476    country country_pkey 
   CONSTRAINT     U   ALTER TABLE ONLY resources.country
    ADD CONSTRAINT country_pkey PRIMARY KEY (id);
 A   ALTER TABLE ONLY resources.country DROP CONSTRAINT country_pkey;
    	   resources            postgres    false    252            �           2606    97478 (   entities_status entities_status_name_key 
   CONSTRAINT     f   ALTER TABLE ONLY resources.entities_status
    ADD CONSTRAINT entities_status_name_key UNIQUE (name);
 U   ALTER TABLE ONLY resources.entities_status DROP CONSTRAINT entities_status_name_key;
    	   resources            postgres    false    254            �           2606    97480 $   entities_status entities_status_pkey 
   CONSTRAINT     e   ALTER TABLE ONLY resources.entities_status
    ADD CONSTRAINT entities_status_pkey PRIMARY KEY (id);
 Q   ALTER TABLE ONLY resources.entities_status DROP CONSTRAINT entities_status_pkey;
    	   resources            postgres    false    254            �           2606    97482     event_roles event_roles_name_key 
   CONSTRAINT     ^   ALTER TABLE ONLY resources.event_roles
    ADD CONSTRAINT event_roles_name_key UNIQUE (name);
 M   ALTER TABLE ONLY resources.event_roles DROP CONSTRAINT event_roles_name_key;
    	   resources            postgres    false    256                       2606    97484    event_roles event_roles_pkey 
   CONSTRAINT     ]   ALTER TABLE ONLY resources.event_roles
    ADD CONSTRAINT event_roles_pkey PRIMARY KEY (id);
 I   ALTER TABLE ONLY resources.event_roles DROP CONSTRAINT event_roles_pkey;
    	   resources            postgres    false    256                       2606    97486 +   events_levels events_levels_description_key 
   CONSTRAINT     p   ALTER TABLE ONLY resources.events_levels
    ADD CONSTRAINT events_levels_description_key UNIQUE (description);
 X   ALTER TABLE ONLY resources.events_levels DROP CONSTRAINT events_levels_description_key;
    	   resources            postgres    false    258                       2606    97488 %   events_levels events_levels_level_key 
   CONSTRAINT     d   ALTER TABLE ONLY resources.events_levels
    ADD CONSTRAINT events_levels_level_key UNIQUE (level);
 R   ALTER TABLE ONLY resources.events_levels DROP CONSTRAINT events_levels_level_key;
    	   resources            postgres    false    258                       2606    97490     events_levels events_levels_pkey 
   CONSTRAINT     a   ALTER TABLE ONLY resources.events_levels
    ADD CONSTRAINT events_levels_pkey PRIMARY KEY (id);
 M   ALTER TABLE ONLY resources.events_levels DROP CONSTRAINT events_levels_pkey;
    	   resources            postgres    false    258            	           2606    97492 +   events_scopes events_scopes_description_key 
   CONSTRAINT     p   ALTER TABLE ONLY resources.events_scopes
    ADD CONSTRAINT events_scopes_description_key UNIQUE (description);
 X   ALTER TABLE ONLY resources.events_scopes DROP CONSTRAINT events_scopes_description_key;
    	   resources            postgres    false    260                       2606    97494     events_scopes events_scopes_pkey 
   CONSTRAINT     a   ALTER TABLE ONLY resources.events_scopes
    ADD CONSTRAINT events_scopes_pkey PRIMARY KEY (id);
 M   ALTER TABLE ONLY resources.events_scopes DROP CONSTRAINT events_scopes_pkey;
    	   resources            postgres    false    260                       2606    97496 %   events_scopes events_scopes_scope_key 
   CONSTRAINT     d   ALTER TABLE ONLY resources.events_scopes
    ADD CONSTRAINT events_scopes_scope_key UNIQUE (scope);
 R   ALTER TABLE ONLY resources.events_scopes DROP CONSTRAINT events_scopes_scope_key;
    	   resources            postgres    false    260                       2606    97498     ext_types ext_types_ext_code_key 
   CONSTRAINT     b   ALTER TABLE ONLY resources.ext_types
    ADD CONSTRAINT ext_types_ext_code_key UNIQUE (ext_code);
 M   ALTER TABLE ONLY resources.ext_types DROP CONSTRAINT ext_types_ext_code_key;
    	   resources            postgres    false    262                       2606    97500    ext_types ext_types_pkey 
   CONSTRAINT     Y   ALTER TABLE ONLY resources.ext_types
    ADD CONSTRAINT ext_types_pkey PRIMARY KEY (id);
 E   ALTER TABLE ONLY resources.ext_types DROP CONSTRAINT ext_types_pkey;
    	   resources            postgres    false    262                       2606    97502 "   jugadores_eeuu jugadores_eeuu_pkey 
   CONSTRAINT     c   ALTER TABLE ONLY resources.jugadores_eeuu
    ADD CONSTRAINT jugadores_eeuu_pkey PRIMARY KEY (id);
 O   ALTER TABLE ONLY resources.jugadores_eeuu DROP CONSTRAINT jugadores_eeuu_pkey;
    	   resources            postgres    false    264                       2606    97504    jugadores_ind jugadores_pkey 
   CONSTRAINT     ]   ALTER TABLE ONLY resources.jugadores_ind
    ADD CONSTRAINT jugadores_pkey PRIMARY KEY (id);
 I   ALTER TABLE ONLY resources.jugadores_ind DROP CONSTRAINT jugadores_pkey;
    	   resources            postgres    false    265                       2606    97506 %   jugadores_ind jugadores_user_name_key 
   CONSTRAINT     g   ALTER TABLE ONLY resources.jugadores_ind
    ADD CONSTRAINT jugadores_user_name_key UNIQUE (username);
 R   ALTER TABLE ONLY resources.jugadores_ind DROP CONSTRAINT jugadores_user_name_key;
    	   resources            postgres    false    265                       2606    97508    packages packages_pkey 
   CONSTRAINT     W   ALTER TABLE ONLY resources.packages
    ADD CONSTRAINT packages_pkey PRIMARY KEY (id);
 C   ALTER TABLE ONLY resources.packages DROP CONSTRAINT packages_pkey;
    	   resources            postgres    false    266                       2606    97510 ,   player_categories player_categories_name_key 
   CONSTRAINT     j   ALTER TABLE ONLY resources.player_categories
    ADD CONSTRAINT player_categories_name_key UNIQUE (name);
 Y   ALTER TABLE ONLY resources.player_categories DROP CONSTRAINT player_categories_name_key;
    	   resources            postgres    false    268                       2606    97512 (   player_categories player_categories_pkey 
   CONSTRAINT     i   ALTER TABLE ONLY resources.player_categories
    ADD CONSTRAINT player_categories_pkey PRIMARY KEY (id);
 U   ALTER TABLE ONLY resources.player_categories DROP CONSTRAINT player_categories_pkey;
    	   resources            postgres    false    268            �           1259    97513    single_profile_id    INDEX     \   CREATE INDEX single_profile_id ON enterprise.profile_users USING btree (single_profile_id);
 )   DROP INDEX enterprise.single_profile_id;
    
   enterprise            postgres    false    217                        2606    97514 6   profile_default_user profile_default_user_city_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY enterprise.profile_default_user
    ADD CONSTRAINT profile_default_user_city_id_fkey FOREIGN KEY (city_id) REFERENCES resources.city(id);
 d   ALTER TABLE ONLY enterprise.profile_default_user DROP CONSTRAINT profile_default_user_city_id_fkey;
    
   enterprise          postgres    false    3831    207    250            !           2606    97519 9   profile_default_user profile_default_user_profile_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY enterprise.profile_default_user
    ADD CONSTRAINT profile_default_user_profile_id_fkey FOREIGN KEY (profile_id) REFERENCES enterprise.profile_member(id);
 g   ALTER TABLE ONLY enterprise.profile_default_user DROP CONSTRAINT profile_default_user_profile_id_fkey;
    
   enterprise          postgres    false    3748    210    207            "           2606    97524 9   profile_default_user profile_default_user_updated_by_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY enterprise.profile_default_user
    ADD CONSTRAINT profile_default_user_updated_by_fkey FOREIGN KEY (updated_by) REFERENCES enterprise.users(username);
 g   ALTER TABLE ONLY enterprise.profile_default_user DROP CONSTRAINT profile_default_user_updated_by_fkey;
    
   enterprise          postgres    false    3771    220    207            #           2606    97529 7   profile_event_admon profile_event_admon_profile_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY enterprise.profile_event_admon
    ADD CONSTRAINT profile_event_admon_profile_id_fkey FOREIGN KEY (profile_id) REFERENCES enterprise.profile_member(id);
 e   ALTER TABLE ONLY enterprise.profile_event_admon DROP CONSTRAINT profile_event_admon_profile_id_fkey;
    
   enterprise          postgres    false    3748    210    208            $           2606    97534 7   profile_event_admon profile_event_admon_updated_by_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY enterprise.profile_event_admon
    ADD CONSTRAINT profile_event_admon_updated_by_fkey FOREIGN KEY (updated_by) REFERENCES enterprise.users(username);
 e   ALTER TABLE ONLY enterprise.profile_event_admon DROP CONSTRAINT profile_event_admon_updated_by_fkey;
    
   enterprise          postgres    false    208    3771    220            %           2606    97539 :   profile_followers profile_followers_profile_follow_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY enterprise.profile_followers
    ADD CONSTRAINT profile_followers_profile_follow_id_fkey FOREIGN KEY (profile_follow_id) REFERENCES enterprise.profile_member(id);
 h   ALTER TABLE ONLY enterprise.profile_followers DROP CONSTRAINT profile_followers_profile_follow_id_fkey;
    
   enterprise          postgres    false    3748    210    209            &           2606    97544 3   profile_followers profile_followers_profile_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY enterprise.profile_followers
    ADD CONSTRAINT profile_followers_profile_id_fkey FOREIGN KEY (profile_id) REFERENCES enterprise.profile_member(id);
 a   ALTER TABLE ONLY enterprise.profile_followers DROP CONSTRAINT profile_followers_profile_id_fkey;
    
   enterprise          postgres    false    3748    209    210            3           2606    97549 +   profile_users profile_id_profile_users_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY enterprise.profile_users
    ADD CONSTRAINT profile_id_profile_users_fkey FOREIGN KEY (profile_id) REFERENCES enterprise.profile_member(id) NOT VALID;
 Y   ALTER TABLE ONLY enterprise.profile_users DROP CONSTRAINT profile_id_profile_users_fkey;
    
   enterprise          postgres    false    217    210    3748            '           2606    97554 *   profile_member profile_member_city_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY enterprise.profile_member
    ADD CONSTRAINT profile_member_city_id_fkey FOREIGN KEY (city_id) REFERENCES resources.city(id);
 X   ALTER TABLE ONLY enterprise.profile_member DROP CONSTRAINT profile_member_city_id_fkey;
    
   enterprise          postgres    false    3831    250    210            (           2606    97559 -   profile_member profile_member_created_by_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY enterprise.profile_member
    ADD CONSTRAINT profile_member_created_by_fkey FOREIGN KEY (created_by) REFERENCES enterprise.users(username);
 [   ALTER TABLE ONLY enterprise.profile_member DROP CONSTRAINT profile_member_created_by_fkey;
    
   enterprise          postgres    false    3771    220    210            )           2606    97564 /   profile_member profile_member_profile_type_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY enterprise.profile_member
    ADD CONSTRAINT profile_member_profile_type_fkey FOREIGN KEY (profile_type) REFERENCES enterprise.profile_type(name);
 ]   ALTER TABLE ONLY enterprise.profile_member DROP CONSTRAINT profile_member_profile_type_fkey;
    
   enterprise          postgres    false    215    3758    210            *           2606    97569 -   profile_member profile_member_updated_by_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY enterprise.profile_member
    ADD CONSTRAINT profile_member_updated_by_fkey FOREIGN KEY (updated_by) REFERENCES enterprise.users(username);
 [   ALTER TABLE ONLY enterprise.profile_member DROP CONSTRAINT profile_member_updated_by_fkey;
    
   enterprise          postgres    false    210    220    3771            +           2606    97574 7   profile_pair_player profile_pair_player_profile_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY enterprise.profile_pair_player
    ADD CONSTRAINT profile_pair_player_profile_id_fkey FOREIGN KEY (profile_id) REFERENCES enterprise.profile_member(id);
 e   ALTER TABLE ONLY enterprise.profile_pair_player DROP CONSTRAINT profile_pair_player_profile_id_fkey;
    
   enterprise          postgres    false    211    210    3748            ,           2606    97579 7   profile_pair_player profile_pair_player_updated_by_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY enterprise.profile_pair_player
    ADD CONSTRAINT profile_pair_player_updated_by_fkey FOREIGN KEY (updated_by) REFERENCES enterprise.users(username);
 e   ALTER TABLE ONLY enterprise.profile_pair_player DROP CONSTRAINT profile_pair_player_updated_by_fkey;
    
   enterprise          postgres    false    220    3771    211            -           2606    97584 /   profile_referee profile_referee_profile_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY enterprise.profile_referee
    ADD CONSTRAINT profile_referee_profile_id_fkey FOREIGN KEY (profile_id) REFERENCES enterprise.profile_member(id);
 ]   ALTER TABLE ONLY enterprise.profile_referee DROP CONSTRAINT profile_referee_profile_id_fkey;
    
   enterprise          postgres    false    212    3748    210            .           2606    97589 /   profile_referee profile_referee_updated_by_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY enterprise.profile_referee
    ADD CONSTRAINT profile_referee_updated_by_fkey FOREIGN KEY (updated_by) REFERENCES enterprise.users(username);
 ]   ALTER TABLE ONLY enterprise.profile_referee DROP CONSTRAINT profile_referee_updated_by_fkey;
    
   enterprise          postgres    false    3771    220    212            /           2606    97594 ;   profile_single_player profile_single_player_profile_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY enterprise.profile_single_player
    ADD CONSTRAINT profile_single_player_profile_id_fkey FOREIGN KEY (profile_id) REFERENCES enterprise.profile_member(id);
 i   ALTER TABLE ONLY enterprise.profile_single_player DROP CONSTRAINT profile_single_player_profile_id_fkey;
    
   enterprise          postgres    false    210    3748    213            0           2606    97599 ;   profile_single_player profile_single_player_updated_by_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY enterprise.profile_single_player
    ADD CONSTRAINT profile_single_player_updated_by_fkey FOREIGN KEY (updated_by) REFERENCES enterprise.users(username);
 i   ALTER TABLE ONLY enterprise.profile_single_player DROP CONSTRAINT profile_single_player_updated_by_fkey;
    
   enterprise          postgres    false    220    3771    213            1           2606    97604 7   profile_team_player profile_team_player_profile_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY enterprise.profile_team_player
    ADD CONSTRAINT profile_team_player_profile_id_fkey FOREIGN KEY (profile_id) REFERENCES enterprise.profile_member(id);
 e   ALTER TABLE ONLY enterprise.profile_team_player DROP CONSTRAINT profile_team_player_profile_id_fkey;
    
   enterprise          postgres    false    3748    210    214            2           2606    97609 7   profile_team_player profile_team_player_updated_by_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY enterprise.profile_team_player
    ADD CONSTRAINT profile_team_player_updated_by_fkey FOREIGN KEY (updated_by) REFERENCES enterprise.users(username);
 e   ALTER TABLE ONLY enterprise.profile_team_player DROP CONSTRAINT profile_team_player_updated_by_fkey;
    
   enterprise          postgres    false    3771    220    214            4           2606    97614 +   profile_users profile_users_created_by_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY enterprise.profile_users
    ADD CONSTRAINT profile_users_created_by_fkey FOREIGN KEY (created_by) REFERENCES enterprise.users(username);
 Y   ALTER TABLE ONLY enterprise.profile_users DROP CONSTRAINT profile_users_created_by_fkey;
    
   enterprise          postgres    false    217    220    3771            5           2606    97619 +   profile_users profile_users_profile_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY enterprise.profile_users
    ADD CONSTRAINT profile_users_profile_id_fkey FOREIGN KEY (profile_id) REFERENCES enterprise.profile_member(id);
 Y   ALTER TABLE ONLY enterprise.profile_users DROP CONSTRAINT profile_users_profile_id_fkey;
    
   enterprise          postgres    false    210    217    3748            6           2606    97624 )   profile_users profile_users_username_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY enterprise.profile_users
    ADD CONSTRAINT profile_users_username_fkey FOREIGN KEY (username) REFERENCES enterprise.users(username);
 W   ALTER TABLE ONLY enterprise.profile_users DROP CONSTRAINT profile_users_username_fkey;
    
   enterprise          postgres    false    220    217    3771            7           2606    97629 /   user_eventroles user_eventroles_created_by_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY enterprise.user_eventroles
    ADD CONSTRAINT user_eventroles_created_by_fkey FOREIGN KEY (created_by) REFERENCES enterprise.users(username);
 ]   ALTER TABLE ONLY enterprise.user_eventroles DROP CONSTRAINT user_eventroles_created_by_fkey;
    
   enterprise          postgres    false    3771    220    218            8           2606    97634 0   user_eventroles user_eventroles_eventrol_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY enterprise.user_eventroles
    ADD CONSTRAINT user_eventroles_eventrol_id_fkey FOREIGN KEY (eventrol_id) REFERENCES resources.event_roles(id);
 ^   ALTER TABLE ONLY enterprise.user_eventroles DROP CONSTRAINT user_eventroles_eventrol_id_fkey;
    
   enterprise          postgres    false    3841    218    256            9           2606    97639    users users_city_id_fkey    FK CONSTRAINT     }   ALTER TABLE ONLY enterprise.users
    ADD CONSTRAINT users_city_id_fkey FOREIGN KEY (city_id) REFERENCES resources.city(id);
 F   ALTER TABLE ONLY enterprise.users DROP CONSTRAINT users_city_id_fkey;
    
   enterprise          postgres    false    220    3831    250            :           2606    97644    users users_country_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY enterprise.users
    ADD CONSTRAINT users_country_id_fkey FOREIGN KEY (country_id) REFERENCES resources.country(id);
 I   ALTER TABLE ONLY enterprise.users DROP CONSTRAINT users_country_id_fkey;
    
   enterprise          postgres    false    220    252    3833            ?           2606    97649 7   domino_boletus_data domino_boletus_data_boletus_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.domino_boletus_data
    ADD CONSTRAINT domino_boletus_data_boletus_id_fkey FOREIGN KEY (boletus_id) REFERENCES events.domino_boletus(id);
 a   ALTER TABLE ONLY events.domino_boletus_data DROP CONSTRAINT domino_boletus_data_boletus_id_fkey;
       events          postgres    false    3773    221    222            @           2606    97654 8   domino_boletus_data domino_boletus_data_win_pair_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.domino_boletus_data
    ADD CONSTRAINT domino_boletus_data_win_pair_id_fkey FOREIGN KEY (win_pair_id) REFERENCES events.domino_rounds_pairs(id);
 b   ALTER TABLE ONLY events.domino_boletus_data DROP CONSTRAINT domino_boletus_data_win_pair_id_fkey;
       events          postgres    false    3785    227    222            A           2606    97659 9   domino_boletus_pairs domino_boletus_pairs_boletus_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.domino_boletus_pairs
    ADD CONSTRAINT domino_boletus_pairs_boletus_id_fkey FOREIGN KEY (boletus_id) REFERENCES events.domino_boletus(id);
 c   ALTER TABLE ONLY events.domino_boletus_pairs DROP CONSTRAINT domino_boletus_pairs_boletus_id_fkey;
       events          postgres    false    221    3773    223            B           2606    97664 7   domino_boletus_pairs domino_boletus_pairs_pairs_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.domino_boletus_pairs
    ADD CONSTRAINT domino_boletus_pairs_pairs_id_fkey FOREIGN KEY (pairs_id) REFERENCES events.domino_rounds_pairs(id);
 a   ALTER TABLE ONLY events.domino_boletus_pairs DROP CONSTRAINT domino_boletus_pairs_pairs_id_fkey;
       events          postgres    false    223    3785    227            �           2606    98172 A   domino_boletus_penalties domino_boletus_penalties_boletus_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.domino_boletus_penalties
    ADD CONSTRAINT domino_boletus_penalties_boletus_id_fkey FOREIGN KEY (boletus_id) REFERENCES events.domino_boletus(id);
 k   ALTER TABLE ONLY events.domino_boletus_penalties DROP CONSTRAINT domino_boletus_penalties_boletus_id_fkey;
       events          postgres    false    221    270    3773            �           2606    98177 >   domino_boletus_penalties domino_boletus_penalties_pair_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.domino_boletus_penalties
    ADD CONSTRAINT domino_boletus_penalties_pair_id_fkey FOREIGN KEY (pair_id) REFERENCES events.domino_rounds_pairs(id);
 h   ALTER TABLE ONLY events.domino_boletus_penalties DROP CONSTRAINT domino_boletus_penalties_pair_id_fkey;
       events          postgres    false    3785    227    270            C           2606    97669 ?   domino_boletus_position domino_boletus_position_boletus_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.domino_boletus_position
    ADD CONSTRAINT domino_boletus_position_boletus_id_fkey FOREIGN KEY (boletus_id) REFERENCES events.domino_boletus(id);
 i   ALTER TABLE ONLY events.domino_boletus_position DROP CONSTRAINT domino_boletus_position_boletus_id_fkey;
       events          postgres    false    3773    221    224            ;           2606    97674 +   domino_boletus domino_boletus_round_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.domino_boletus
    ADD CONSTRAINT domino_boletus_round_id_fkey FOREIGN KEY (round_id) REFERENCES events.domino_rounds(id);
 U   ALTER TABLE ONLY events.domino_boletus DROP CONSTRAINT domino_boletus_round_id_fkey;
       events          postgres    false    226    3783    221            <           2606    97679 ,   domino_boletus domino_boletus_status_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.domino_boletus
    ADD CONSTRAINT domino_boletus_status_id_fkey FOREIGN KEY (status_id) REFERENCES resources.entities_status(id);
 V   ALTER TABLE ONLY events.domino_boletus DROP CONSTRAINT domino_boletus_status_id_fkey;
       events          postgres    false    3837    221    254            =           2606    97684 +   domino_boletus domino_boletus_table_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.domino_boletus
    ADD CONSTRAINT domino_boletus_table_id_fkey FOREIGN KEY (table_id) REFERENCES events.domino_tables(id);
 U   ALTER TABLE ONLY events.domino_boletus DROP CONSTRAINT domino_boletus_table_id_fkey;
       events          postgres    false    229    221    3789            >           2606    97689 -   domino_boletus domino_boletus_tourney_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.domino_boletus
    ADD CONSTRAINT domino_boletus_tourney_id_fkey FOREIGN KEY (tourney_id) REFERENCES events.tourney(id);
 W   ALTER TABLE ONLY events.domino_boletus DROP CONSTRAINT domino_boletus_tourney_id_fkey;
       events          postgres    false    3811    221    240            D           2606    97694 3   domino_categories domino_categories_tourney_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.domino_categories
    ADD CONSTRAINT domino_categories_tourney_id_fkey FOREIGN KEY (tourney_id) REFERENCES events.tourney(id);
 ]   ALTER TABLE ONLY events.domino_categories DROP CONSTRAINT domino_categories_tourney_id_fkey;
       events          postgres    false    3811    225    240            E           2606    97699 +   domino_rounds domino_rounds_created_by_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.domino_rounds
    ADD CONSTRAINT domino_rounds_created_by_fkey FOREIGN KEY (created_by) REFERENCES enterprise.users(username);
 U   ALTER TABLE ONLY events.domino_rounds DROP CONSTRAINT domino_rounds_created_by_fkey;
       events          postgres    false    226    220    3771            I           2606    97704 7   domino_rounds_pairs domino_rounds_pairs_created_by_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.domino_rounds_pairs
    ADD CONSTRAINT domino_rounds_pairs_created_by_fkey FOREIGN KEY (created_by) REFERENCES enterprise.users(username);
 a   ALTER TABLE ONLY events.domino_rounds_pairs DROP CONSTRAINT domino_rounds_pairs_created_by_fkey;
       events          postgres    false    3771    227    220            J           2606    97709 :   domino_rounds_pairs domino_rounds_pairs_one_player_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.domino_rounds_pairs
    ADD CONSTRAINT domino_rounds_pairs_one_player_id_fkey FOREIGN KEY (one_player_id) REFERENCES enterprise.profile_member(id);
 d   ALTER TABLE ONLY events.domino_rounds_pairs DROP CONSTRAINT domino_rounds_pairs_one_player_id_fkey;
       events          postgres    false    3748    227    210            K           2606    97714 6   domino_rounds_pairs domino_rounds_pairs_player_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.domino_rounds_pairs
    ADD CONSTRAINT domino_rounds_pairs_player_id_fkey FOREIGN KEY (player_id) REFERENCES events.players(id);
 `   ALTER TABLE ONLY events.domino_rounds_pairs DROP CONSTRAINT domino_rounds_pairs_player_id_fkey;
       events          postgres    false    3803    227    235            L           2606    97719 5   domino_rounds_pairs domino_rounds_pairs_round_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.domino_rounds_pairs
    ADD CONSTRAINT domino_rounds_pairs_round_id_fkey FOREIGN KEY (round_id) REFERENCES events.domino_rounds(id);
 _   ALTER TABLE ONLY events.domino_rounds_pairs DROP CONSTRAINT domino_rounds_pairs_round_id_fkey;
       events          postgres    false    226    227    3783            M           2606    97724 7   domino_rounds_pairs domino_rounds_pairs_tourney_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.domino_rounds_pairs
    ADD CONSTRAINT domino_rounds_pairs_tourney_id_fkey FOREIGN KEY (tourney_id) REFERENCES events.tourney(id);
 a   ALTER TABLE ONLY events.domino_rounds_pairs DROP CONSTRAINT domino_rounds_pairs_tourney_id_fkey;
       events          postgres    false    240    3811    227            N           2606    97729 :   domino_rounds_pairs domino_rounds_pairs_two_player_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.domino_rounds_pairs
    ADD CONSTRAINT domino_rounds_pairs_two_player_id_fkey FOREIGN KEY (two_player_id) REFERENCES enterprise.profile_member(id);
 d   ALTER TABLE ONLY events.domino_rounds_pairs DROP CONSTRAINT domino_rounds_pairs_two_player_id_fkey;
       events          postgres    false    3748    210    227            O           2606    97734 7   domino_rounds_pairs domino_rounds_pairs_updated_by_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.domino_rounds_pairs
    ADD CONSTRAINT domino_rounds_pairs_updated_by_fkey FOREIGN KEY (updated_by) REFERENCES enterprise.users(username);
 a   ALTER TABLE ONLY events.domino_rounds_pairs DROP CONSTRAINT domino_rounds_pairs_updated_by_fkey;
       events          postgres    false    3771    227    220            P           2606    97739 6   domino_rounds_scale domino_rounds_scale_player_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.domino_rounds_scale
    ADD CONSTRAINT domino_rounds_scale_player_id_fkey FOREIGN KEY (player_id) REFERENCES events.players(id);
 `   ALTER TABLE ONLY events.domino_rounds_scale DROP CONSTRAINT domino_rounds_scale_player_id_fkey;
       events          postgres    false    235    228    3803            Q           2606    97744 5   domino_rounds_scale domino_rounds_scale_round_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.domino_rounds_scale
    ADD CONSTRAINT domino_rounds_scale_round_id_fkey FOREIGN KEY (round_id) REFERENCES events.domino_rounds(id);
 _   ALTER TABLE ONLY events.domino_rounds_scale DROP CONSTRAINT domino_rounds_scale_round_id_fkey;
       events          postgres    false    226    3783    228            R           2606    97749 7   domino_rounds_scale domino_rounds_scale_tourney_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.domino_rounds_scale
    ADD CONSTRAINT domino_rounds_scale_tourney_id_fkey FOREIGN KEY (tourney_id) REFERENCES events.tourney(id);
 a   ALTER TABLE ONLY events.domino_rounds_scale DROP CONSTRAINT domino_rounds_scale_tourney_id_fkey;
       events          postgres    false    228    3811    240            F           2606    97754 *   domino_rounds domino_rounds_status_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.domino_rounds
    ADD CONSTRAINT domino_rounds_status_id_fkey FOREIGN KEY (status_id) REFERENCES resources.entities_status(id);
 T   ALTER TABLE ONLY events.domino_rounds DROP CONSTRAINT domino_rounds_status_id_fkey;
       events          postgres    false    226    254    3837            G           2606    97759 +   domino_rounds domino_rounds_tourney_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.domino_rounds
    ADD CONSTRAINT domino_rounds_tourney_id_fkey FOREIGN KEY (tourney_id) REFERENCES events.tourney(id);
 U   ALTER TABLE ONLY events.domino_rounds DROP CONSTRAINT domino_rounds_tourney_id_fkey;
       events          postgres    false    3811    240    226            H           2606    97764 +   domino_rounds domino_rounds_updated_by_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.domino_rounds
    ADD CONSTRAINT domino_rounds_updated_by_fkey FOREIGN KEY (updated_by) REFERENCES enterprise.users(username);
 U   ALTER TABLE ONLY events.domino_rounds DROP CONSTRAINT domino_rounds_updated_by_fkey;
       events          postgres    false    226    3771    220            S           2606    97769 +   domino_tables domino_tables_created_by_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.domino_tables
    ADD CONSTRAINT domino_tables_created_by_fkey FOREIGN KEY (created_by) REFERENCES enterprise.users(username);
 U   ALTER TABLE ONLY events.domino_tables DROP CONSTRAINT domino_tables_created_by_fkey;
       events          postgres    false    3771    229    220            V           2606    97774 5   domino_tables_files domino_tables_files_table_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.domino_tables_files
    ADD CONSTRAINT domino_tables_files_table_id_fkey FOREIGN KEY (table_id) REFERENCES events.domino_tables(id);
 _   ALTER TABLE ONLY events.domino_tables_files DROP CONSTRAINT domino_tables_files_table_id_fkey;
       events          postgres    false    3789    230    229            T           2606    97779 +   domino_tables domino_tables_tourney_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.domino_tables
    ADD CONSTRAINT domino_tables_tourney_id_fkey FOREIGN KEY (tourney_id) REFERENCES events.tourney(id);
 U   ALTER TABLE ONLY events.domino_tables DROP CONSTRAINT domino_tables_tourney_id_fkey;
       events          postgres    false    229    240    3811            U           2606    97784 +   domino_tables domino_tables_updated_by_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.domino_tables
    ADD CONSTRAINT domino_tables_updated_by_fkey FOREIGN KEY (updated_by) REFERENCES enterprise.users(username);
 U   ALTER TABLE ONLY events.domino_tables DROP CONSTRAINT domino_tables_updated_by_fkey;
       events          postgres    false    220    3771    229            W           2606    97789    events events_city_id_fkey    FK CONSTRAINT     {   ALTER TABLE ONLY events.events
    ADD CONSTRAINT events_city_id_fkey FOREIGN KEY (city_id) REFERENCES resources.city(id);
 D   ALTER TABLE ONLY events.events DROP CONSTRAINT events_city_id_fkey;
       events          postgres    false    231    3831    250            X           2606    97794    events events_created_by_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.events
    ADD CONSTRAINT events_created_by_fkey FOREIGN KEY (created_by) REFERENCES enterprise.users(username);
 G   ALTER TABLE ONLY events.events DROP CONSTRAINT events_created_by_fkey;
       events          postgres    false    231    3771    220            \           2606    97799 1   events_followers events_followers_profile_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.events_followers
    ADD CONSTRAINT events_followers_profile_id_fkey FOREIGN KEY (profile_id) REFERENCES enterprise.profile_member(id);
 [   ALTER TABLE ONLY events.events_followers DROP CONSTRAINT events_followers_profile_id_fkey;
       events          postgres    false    232    3748    210            Y           2606    97804    events events_status_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.events
    ADD CONSTRAINT events_status_id_fkey FOREIGN KEY (status_id) REFERENCES resources.entities_status(id);
 F   ALTER TABLE ONLY events.events DROP CONSTRAINT events_status_id_fkey;
       events          postgres    false    3837    254    231            Z           2606    97809    events events_updated_by_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.events
    ADD CONSTRAINT events_updated_by_fkey FOREIGN KEY (updated_by) REFERENCES enterprise.users(username);
 G   ALTER TABLE ONLY events.events DROP CONSTRAINT events_updated_by_fkey;
       events          postgres    false    220    3771    231            ]           2606    97814 '   invitations invitations_created_by_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.invitations
    ADD CONSTRAINT invitations_created_by_fkey FOREIGN KEY (created_by) REFERENCES enterprise.users(username);
 Q   ALTER TABLE ONLY events.invitations DROP CONSTRAINT invitations_created_by_fkey;
       events          postgres    false    220    3771    234            ^           2606    97819 '   invitations invitations_profile_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.invitations
    ADD CONSTRAINT invitations_profile_id_fkey FOREIGN KEY (profile_id) REFERENCES enterprise.profile_member(id);
 Q   ALTER TABLE ONLY events.invitations DROP CONSTRAINT invitations_profile_id_fkey;
       events          postgres    false    210    3748    234            _           2606    97824 (   invitations invitations_status_name_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.invitations
    ADD CONSTRAINT invitations_status_name_fkey FOREIGN KEY (status_name) REFERENCES resources.entities_status(name);
 R   ALTER TABLE ONLY events.invitations DROP CONSTRAINT invitations_status_name_fkey;
       events          postgres    false    3835    254    234            `           2606    97829 '   invitations invitations_updated_by_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.invitations
    ADD CONSTRAINT invitations_updated_by_fkey FOREIGN KEY (updated_by) REFERENCES enterprise.users(username);
 Q   ALTER TABLE ONLY events.invitations DROP CONSTRAINT invitations_updated_by_fkey;
       events          postgres    false    234    3771    220            a           2606    97834    players players_created_by_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.players
    ADD CONSTRAINT players_created_by_fkey FOREIGN KEY (created_by) REFERENCES enterprise.users(username);
 I   ALTER TABLE ONLY events.players DROP CONSTRAINT players_created_by_fkey;
       events          postgres    false    3771    220    235            g           2606    97839    players_users players_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.players_users
    ADD CONSTRAINT players_id_fkey FOREIGN KEY (player_id) REFERENCES events.players(id);
 G   ALTER TABLE ONLY events.players_users DROP CONSTRAINT players_id_fkey;
       events          postgres    false    3803    236    235            b           2606    97844 "   players players_invitation_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.players
    ADD CONSTRAINT players_invitation_id_fkey FOREIGN KEY (invitation_id) REFERENCES events.invitations(id);
 L   ALTER TABLE ONLY events.players DROP CONSTRAINT players_invitation_id_fkey;
       events          postgres    false    235    3801    234            c           2606    97849    players players_profile_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.players
    ADD CONSTRAINT players_profile_id_fkey FOREIGN KEY (profile_id) REFERENCES enterprise.profile_member(id);
 I   ALTER TABLE ONLY events.players DROP CONSTRAINT players_profile_id_fkey;
       events          postgres    false    235    3748    210            h           2606    97854 %   players_users players_profile_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.players_users
    ADD CONSTRAINT players_profile_id_fkey FOREIGN KEY (profile_id) REFERENCES enterprise.profile_member(id);
 O   ALTER TABLE ONLY events.players_users DROP CONSTRAINT players_profile_id_fkey;
       events          postgres    false    210    236    3748            d           2606    97859    players players_status_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.players
    ADD CONSTRAINT players_status_id_fkey FOREIGN KEY (status_id) REFERENCES resources.entities_status(id);
 H   ALTER TABLE ONLY events.players DROP CONSTRAINT players_status_id_fkey;
       events          postgres    false    254    235    3837            e           2606    97864    players players_tourney_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.players
    ADD CONSTRAINT players_tourney_id_fkey FOREIGN KEY (tourney_id) REFERENCES events.tourney(id);
 I   ALTER TABLE ONLY events.players DROP CONSTRAINT players_tourney_id_fkey;
       events          postgres    false    240    3811    235            f           2606    97869    players players_updated_by_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.players
    ADD CONSTRAINT players_updated_by_fkey FOREIGN KEY (updated_by) REFERENCES enterprise.users(username);
 I   ALTER TABLE ONLY events.players DROP CONSTRAINT players_updated_by_fkey;
       events          postgres    false    220    235    3771            [           2606    97874    events profile_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.events
    ADD CONSTRAINT profile_id_fkey FOREIGN KEY (profile_id) REFERENCES enterprise.profile_member(id) NOT VALID;
 @   ALTER TABLE ONLY events.events DROP CONSTRAINT profile_id_fkey;
       events          postgres    false    231    3748    210            i           2606    97879 !   referees referees_created_by_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.referees
    ADD CONSTRAINT referees_created_by_fkey FOREIGN KEY (created_by) REFERENCES enterprise.users(username);
 K   ALTER TABLE ONLY events.referees DROP CONSTRAINT referees_created_by_fkey;
       events          postgres    false    220    237    3771            j           2606    97884 $   referees referees_invitation_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.referees
    ADD CONSTRAINT referees_invitation_id_fkey FOREIGN KEY (invitation_id) REFERENCES events.invitations(id);
 N   ALTER TABLE ONLY events.referees DROP CONSTRAINT referees_invitation_id_fkey;
       events          postgres    false    3801    237    234            k           2606    97889 !   referees referees_profile_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.referees
    ADD CONSTRAINT referees_profile_id_fkey FOREIGN KEY (profile_id) REFERENCES enterprise.profile_member(id);
 K   ALTER TABLE ONLY events.referees DROP CONSTRAINT referees_profile_id_fkey;
       events          postgres    false    3748    210    237            l           2606    97894     referees referees_status_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.referees
    ADD CONSTRAINT referees_status_id_fkey FOREIGN KEY (status_id) REFERENCES resources.entities_status(id);
 J   ALTER TABLE ONLY events.referees DROP CONSTRAINT referees_status_id_fkey;
       events          postgres    false    237    254    3837            m           2606    97899 !   referees referees_tourney_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.referees
    ADD CONSTRAINT referees_tourney_id_fkey FOREIGN KEY (tourney_id) REFERENCES events.tourney(id);
 K   ALTER TABLE ONLY events.referees DROP CONSTRAINT referees_tourney_id_fkey;
       events          postgres    false    237    3811    240            n           2606    97904 !   referees referees_updated_by_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.referees
    ADD CONSTRAINT referees_updated_by_fkey FOREIGN KEY (updated_by) REFERENCES enterprise.users(username);
 K   ALTER TABLE ONLY events.referees DROP CONSTRAINT referees_updated_by_fkey;
       events          postgres    false    3771    220    237            o           2606    97909    tourney tourney_created_by_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.tourney
    ADD CONSTRAINT tourney_created_by_fkey FOREIGN KEY (created_by) REFERENCES enterprise.users(username);
 I   ALTER TABLE ONLY events.tourney DROP CONSTRAINT tourney_created_by_fkey;
       events          postgres    false    220    240    3771            p           2606    97914    tourney tourney_event_id_fkey    FK CONSTRAINT     ~   ALTER TABLE ONLY events.tourney
    ADD CONSTRAINT tourney_event_id_fkey FOREIGN KEY (event_id) REFERENCES events.events(id);
 G   ALTER TABLE ONLY events.tourney DROP CONSTRAINT tourney_event_id_fkey;
       events          postgres    false    240    231    3793            q           2606    97919    tourney tourney_profile_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.tourney
    ADD CONSTRAINT tourney_profile_id_fkey FOREIGN KEY (profile_id) REFERENCES enterprise.profile_member(id);
 I   ALTER TABLE ONLY events.tourney DROP CONSTRAINT tourney_profile_id_fkey;
       events          postgres    false    210    240    3748            r           2606    97924    tourney tourney_status_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.tourney
    ADD CONSTRAINT tourney_status_id_fkey FOREIGN KEY (status_id) REFERENCES resources.entities_status(id) NOT VALID;
 H   ALTER TABLE ONLY events.tourney DROP CONSTRAINT tourney_status_id_fkey;
       events          postgres    false    3837    240    254            s           2606    97929    tourney tourney_updated_by_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.tourney
    ADD CONSTRAINT tourney_updated_by_fkey FOREIGN KEY (updated_by) REFERENCES enterprise.users(username);
 I   ALTER TABLE ONLY events.tourney DROP CONSTRAINT tourney_updated_by_fkey;
       events          postgres    false    220    240    3771            t           2606    97934 8   trace_lottery_manual trace_lottery_manual_player_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.trace_lottery_manual
    ADD CONSTRAINT trace_lottery_manual_player_id_fkey FOREIGN KEY (player_id) REFERENCES events.players(id);
 b   ALTER TABLE ONLY events.trace_lottery_manual DROP CONSTRAINT trace_lottery_manual_player_id_fkey;
       events          postgres    false    235    241    3803            u           2606    97939 9   trace_lottery_manual trace_lottery_manual_tourney_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY events.trace_lottery_manual
    ADD CONSTRAINT trace_lottery_manual_tourney_id_fkey FOREIGN KEY (tourney_id) REFERENCES events.tourney(id);
 c   ALTER TABLE ONLY events.trace_lottery_manual DROP CONSTRAINT trace_lottery_manual_tourney_id_fkey;
       events          postgres    false    240    241    3811            v           2606    97944 +   notifications notifications_created_by_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY notifications.notifications
    ADD CONSTRAINT notifications_created_by_fkey FOREIGN KEY (created_by) REFERENCES enterprise.users(username);
 \   ALTER TABLE ONLY notifications.notifications DROP CONSTRAINT notifications_created_by_fkey;
       notifications          postgres    false    242    220    3771            w           2606    97949 +   notifications notifications_profile_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY notifications.notifications
    ADD CONSTRAINT notifications_profile_id_fkey FOREIGN KEY (profile_id) REFERENCES enterprise.profile_member(id);
 \   ALTER TABLE ONLY notifications.notifications DROP CONSTRAINT notifications_profile_id_fkey;
       notifications          postgres    false    3748    242    210            x           2606    97954 1   comment_comments comment_comments_comment_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY post.comment_comments
    ADD CONSTRAINT comment_comments_comment_id_fkey FOREIGN KEY (comment_id) REFERENCES post.post_comments(id);
 Y   ALTER TABLE ONLY post.comment_comments DROP CONSTRAINT comment_comments_comment_id_fkey;
       post          postgres    false    246    243    3823            y           2606    97959 1   comment_comments comment_comments_created_by_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY post.comment_comments
    ADD CONSTRAINT comment_comments_created_by_fkey FOREIGN KEY (created_by) REFERENCES enterprise.users(username);
 Y   ALTER TABLE ONLY post.comment_comments DROP CONSTRAINT comment_comments_created_by_fkey;
       post          postgres    false    243    3771    220            {           2606    97964 +   comment_likes comment_likes_comment_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY post.comment_likes
    ADD CONSTRAINT comment_likes_comment_id_fkey FOREIGN KEY (comment_id) REFERENCES post.post_comments(id);
 S   ALTER TABLE ONLY post.comment_likes DROP CONSTRAINT comment_likes_comment_id_fkey;
       post          postgres    false    3823    246    244            |           2606    97969 +   comment_likes comment_likes_created_by_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY post.comment_likes
    ADD CONSTRAINT comment_likes_created_by_fkey FOREIGN KEY (created_by) REFERENCES enterprise.users(username);
 S   ALTER TABLE ONLY post.comment_likes DROP CONSTRAINT comment_likes_created_by_fkey;
       post          postgres    false    3771    220    244            �           2606    97974 +   post_comments post_comments_created_by_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY post.post_comments
    ADD CONSTRAINT post_comments_created_by_fkey FOREIGN KEY (created_by) REFERENCES enterprise.users(username);
 S   ALTER TABLE ONLY post.post_comments DROP CONSTRAINT post_comments_created_by_fkey;
       post          postgres    false    246    220    3771            �           2606    97979 (   post_comments post_comments_post_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY post.post_comments
    ADD CONSTRAINT post_comments_post_id_fkey FOREIGN KEY (post_id) REFERENCES post.post(id);
 P   ALTER TABLE ONLY post.post_comments DROP CONSTRAINT post_comments_post_id_fkey;
       post          postgres    false    246    3821    245            ~           2606    97984    post post_created_by_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY post.post
    ADD CONSTRAINT post_created_by_fkey FOREIGN KEY (created_by) REFERENCES enterprise.users(username);
 A   ALTER TABLE ONLY post.post DROP CONSTRAINT post_created_by_fkey;
       post          postgres    false    220    245    3771            �           2606    97989 "   post_files post_files_post_id_fkey    FK CONSTRAINT     |   ALTER TABLE ONLY post.post_files
    ADD CONSTRAINT post_files_post_id_fkey FOREIGN KEY (post_id) REFERENCES post.post(id);
 J   ALTER TABLE ONLY post.post_files DROP CONSTRAINT post_files_post_id_fkey;
       post          postgres    false    3821    247    245            �           2606    97994 %   post_likes post_likes_created_by_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY post.post_likes
    ADD CONSTRAINT post_likes_created_by_fkey FOREIGN KEY (created_by) REFERENCES enterprise.users(username);
 M   ALTER TABLE ONLY post.post_likes DROP CONSTRAINT post_likes_created_by_fkey;
       post          postgres    false    220    3771    248            �           2606    97999 "   post_likes post_likes_post_id_fkey    FK CONSTRAINT     |   ALTER TABLE ONLY post.post_likes
    ADD CONSTRAINT post_likes_post_id_fkey FOREIGN KEY (post_id) REFERENCES post.post(id);
 J   ALTER TABLE ONLY post.post_likes DROP CONSTRAINT post_likes_post_id_fkey;
       post          postgres    false    248    3821    245                       2606    98004    post post_updated_by_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY post.post
    ADD CONSTRAINT post_updated_by_fkey FOREIGN KEY (updated_by) REFERENCES enterprise.users(username);
 A   ALTER TABLE ONLY post.post DROP CONSTRAINT post_updated_by_fkey;
       post          postgres    false    3771    220    245            z           2606    98009 1   comment_comments profile_id_comment_comments_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY post.comment_comments
    ADD CONSTRAINT profile_id_comment_comments_fkey FOREIGN KEY (profile_id) REFERENCES enterprise.profile_member(id) NOT VALID;
 Y   ALTER TABLE ONLY post.comment_comments DROP CONSTRAINT profile_id_comment_comments_fkey;
       post          postgres    false    210    3748    243            }           2606    98014 +   comment_likes profile_id_comment_likes_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY post.comment_likes
    ADD CONSTRAINT profile_id_comment_likes_fkey FOREIGN KEY (profile_id) REFERENCES enterprise.profile_member(id) NOT VALID;
 S   ALTER TABLE ONLY post.comment_likes DROP CONSTRAINT profile_id_comment_likes_fkey;
       post          postgres    false    244    3748    210            �           2606    98019 +   post_comments profile_id_post_comments_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY post.post_comments
    ADD CONSTRAINT profile_id_post_comments_fkey FOREIGN KEY (profile_id) REFERENCES enterprise.profile_member(id) NOT VALID;
 S   ALTER TABLE ONLY post.post_comments DROP CONSTRAINT profile_id_post_comments_fkey;
       post          postgres    false    210    246    3748            �           2606    98024 %   post_likes profile_id_post_likes_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY post.post_likes
    ADD CONSTRAINT profile_id_post_likes_fkey FOREIGN KEY (profile_id) REFERENCES enterprise.profile_member(id) NOT VALID;
 M   ALTER TABLE ONLY post.post_likes DROP CONSTRAINT profile_id_post_likes_fkey;
       post          postgres    false    3748    210    248            �           2606    98029    post profile_id_psot_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY post.post
    ADD CONSTRAINT profile_id_psot_fkey FOREIGN KEY (profile_id) REFERENCES enterprise.profile_member(id) NOT VALID;
 A   ALTER TABLE ONLY post.post DROP CONSTRAINT profile_id_psot_fkey;
       post          postgres    false    3748    245    210            �           2606    98034    city city_country_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY resources.city
    ADD CONSTRAINT city_country_id_fkey FOREIGN KEY (country_id) REFERENCES resources.country(id);
 F   ALTER TABLE ONLY resources.city DROP CONSTRAINT city_country_id_fkey;
    	   resources          postgres    false    252    250    3833            �           2606    98039 .   player_categories player_categories_scope_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY resources.player_categories
    ADD CONSTRAINT player_categories_scope_fkey FOREIGN KEY (scope) REFERENCES resources.events_scopes(id);
 [   ALTER TABLE ONLY resources.player_categories DROP CONSTRAINT player_categories_scope_fkey;
    	   resources          postgres    false    268    3851    260            
      x������ � �            x������ � �            x������ � �            x������ � �            x������ � �            x������ � �            x������ � �            x������ � �         �   x���An�0E��)� 4;+��D��J�*U��V����/�I^����D��S��MI_��v��b0~��:+1�#����8Ӏ�~HVq�"�"��$���G����4��F��d��C��g��I}N�>"Cj��7j	ۺg-���F55Z�Ħ����P[#����A��3�q�s��p���_���fWW@�I鹤����>����Dy-�f�-<���"��            x������ � �            x������ � �            x������ � �            x������ � �            x������ � �            x������ � �            x������ � �      I      x������ � �            x������ � �            x������ � �            x������ � �            x������ � �            x������ � �             x������ � �      !      x������ � �      "      x������ � �      #      x������ � �      $      x������ � �      %      x������ � �      &      x������ � �      '      x������ � �      (      x������ � �      )      x������ � �      +      x������ � �      ,      x������ � �      -      x������ � �      .      x������ � �      /      x������ � �      0      x������ � �      1      x������ � �      2      x������ � �      3      x������ � �      4      x�3763I4H4517������ &z�      5   �   x�-�AN�0EדS��6-K�E	QĊ͏�F��	8v���(�7`�1d�������m���u�H�R��gψ���y)�a�t����	W��CV��	g��3����	���Л�	��pK{p�f��OYm���K7�iS�O>��ZjУ+����k�9�.h7�.�+/i�����c��&��^�6ˠ�0z��]��(E�&�C>9N�����H`�߯���-3[p      7   L   x�3�t.MJ�,�2�t*J,��2�9��s�s�29ӸL8]C������E%�
A���@��kqA�� �1z\\\ �S�      9   S  x����N�0��?����埳ڕ�"aé�"N�Ȣ^�e;ٖI���y�y�a`�+>֕�}۪���e b`_�^h�!�L+@��hD"V�Δ"���n�,`4a<���e}�eC$�eEU#���́%Of���e7������qC���e;��\���t��e�u��A���NV���U���D"�G�5U���|�:"��C��m�����F]u0:f�����c�f��]��\��1�1}��F6�,1,|�XSu��^�m��	ڂ��K>���)���/��C����Z�Q�g_�g�mau"'�i~v�$�ꪐS«�i�@��3      ;   ]   x�3��q�t��
uwt���M/�4202�50�54R00�#.#� W7� WWN� 'ϐ �*�9��C��}<�C8\�<�]�,G��c���� ]ta      =      x�3�4A.#N0�2�C�=... 4#p      ?   8   x�3���OŃ��\F�~�ə�y@�a�g`�e��W�Z�D���q��qqq �      A   �   x�����@E���*l 2�Z�@p�'C v�V��99�d�ͯ7����]��䤏��R7�v�1s�Hp/3i��&ʓ�6z��Yw���kZ��3t�I�,��ðg{�.L�#�4*��M!��6�| ���      C   G  x�uU�r�F<�|��Ņ} $�2D�N��C�J�ʗ�7^�F@��7��T>A?��e��ڵ.T�N�t��4l)���g0��O�`U��	R��ug�����<U���
���5�G�ɻ(Q���t�c����]a	?������>�Q`��qp�@q�r)V�K؄h���~�!�S�
���e���h�Mک�XCCхޙ��wfZ�$^%��FQ<A�LLT�x�~��i�F!��h�W�pm���
�zQ�4��f�BÞ�F���cHu�����,��8;��:������6�L'�Öp�h=4��m�i�`k�����^+5w1�yz�6%%P���bW��Oc��8�R(4�h����9Jq�
��_�s��p�R����(5��G��ae���d�<�Sߟ�(�g]S�͠)�KxG1�>c�bb�D��Vpٷ�+�L�6U�Aװ����v���FU|[��K���'�gZ�
T�Mk;^`�Us�)�����p��Q�2��"�1�`g�$�~��9Jyr+k-�x�5wQ�BU2�&��o=[٥D�
.�a'нɬ�-�M�� �1#���4�m	�$É���[��D1���B�z�7��G7�R2�R�����f��}J�ZΜ��c�D֨ճ��i9(<FÎ��<��a7>���b�T��wْ{�;-�N�1�?p^��g2M3"���׳5��)"�B��3���
���8�k8!�0�x�r���,`c�q�3X��}CF���)n�E��S$_���Ha����&d��K,5<NNt��r��y�e���d����\
i���]�5���)_�dV��e ���/��X��_#�Fr��      D   �  x����n�F�ϳO�'X��dIGEI`'�ݦ������\gI�����r(z+zӋ���R옭aؚ�P3���RN��Zuٵ����!��O�쯶��DW�h��c+M��ZP��M�?�ӌ�Q]#���Vw��"�����r���#Vҵ��R�"{%#�LV&/_@��A�X�s��I2�lJoŽ�&;��Z�2�Eu%�Zn4}q��Q�6��C���V��*���^�P8J��	�~�N�7�yZ�6"��G"/�j6��W��I� �k�ʍ�78��U2sv���9]H�
S��Lvwb�Z��̃R4�J��,�љ��W�sr-���(�a�J��$���Gc^�%��wD�JT�ƻ�HQ�Q� �3���Y����y-�T-��M&��p��#����9}P�=��[�����"�`��Q.�|���w��q��M+�^�Xd���]�)$�􊑰��xcyI��Ne���� S���@����� 
��X����$Y.
�Oq*�+��Ob�t��
�x��N����|�O��C��:o7e�:�Q��|D+i<��w�Z�n7R�� l�E�e�/��a��,��<�Km�T�^��w�z��5樰ju����L9�>g���ɺ�mv%{et#ѐ<����)l�N�����YR ���5U¶��nP{]v��[�d�5��=�s9%߄7}���%�TLYaKt�-.�|�6�z�P"8�)2��&-�Q�T��.f�Ŵ`E�ϙ�{ ��]�����\����s�gǨ,P�;)����0(̃� @�S�8}D'�IX%_�gG��sV�O�\�J�=sx���4��ϲ`��Z]W�3������c��=ϟ�Ӓ3Z�z-�&�B��Q}�t3�m.F�-���{���Yq�ŧQ�a��Z�۾�l���M��r�?p�Ϡ4G8�[�N̰�� �	LS�.VN��^3��Z�[���]�y�
���a�8��P_�K:S�]��z��G�Es^AI���~�t�sҽ�#g�~��QYN���������8G1genۯĜA>֍�$��[�9%N�۶�U<iƣ>ae� ���*$��������=�J��c�E�"th7Xf���z@�6?,�g���)RZ�:;f�As�<~�ƴU�[���r�ʙM�A��> >ϼx5�B�V����MYy�s�9/�.��	��"J&%�t*zQ;l����'��s��O�vJ��N4�� �x����r��{>�(Yi�v)��u[��?��3OF-/Y��w���fWF�]wN�ȱ����g����c���N��=�����b��Ô0E��x-WIc��"?a�<̝+	mv��{&�#��d7g��7�׺��o��e��
��J�
i����a{?(yJ��G��J�i��>\�lZb%J��nxM�u�6e	�,yj�`�DL�>q�>��$V��:�'���%��c��B�d      E   S   x�3�t-K�+�/V�/�K�N�g&�sp�a	gnfQ%������������&���̴���"NSN#0L������ ��      G   �   x�=�A
�0���)z�L��.J��t�B�����#J���^R�Ӝb^GxxkA��F�L}�r&p��Fb>��:,�qHZ؅Z8���;毮Pus��!��8汬��;����`�8.kٔ��m��4���O��n�g�1�Q>2X     