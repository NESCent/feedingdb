PGDMP                 	        r           feed    8.4.20    8.4.20 Y   �	           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                       false            �	           0    0 
   STDSTRINGS 
   STDSTRINGS     )   SET standard_conforming_strings = 'off';
                       false            �	           1262    16409    feed    DATABASE     v   CREATE DATABASE feed WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8';
    DROP DATABASE feed;
             postgres    false                        2615    2200    public    SCHEMA        CREATE SCHEMA public;
    DROP SCHEMA public;
             postgres    false            �	           0    0    SCHEMA public    COMMENT     6   COMMENT ON SCHEMA public IS 'standard public schema';
                  postgres    false    6            �	           0    0    public    ACL     �   REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO feeding_app;
GRANT ALL ON SCHEMA public TO PUBLIC;
                  postgres    false    6                       2612    16541    plpgsql    PROCEDURAL LANGUAGE     $   CREATE PROCEDURAL LANGUAGE plpgsql;
 "   DROP PROCEDURAL LANGUAGE plpgsql;
             postgres    false            �            1255    16542     pg_grant(text, text, text, text)    FUNCTION       CREATE FUNCTION pg_grant(usr text, prv text, ptrn text, nsp text) RETURNS integer
    LANGUAGE plpgsql
    AS $$
 DECLARE
   obj record;
   num integer;
 BEGIN
   num:=0;
   FOR obj IN SELECT relname FROM pg_class c
     JOIN pg_namespace ns ON (c.relnamespace = ns.oid) WHERE
     relkind IN ('r','v','S') AND
         nspname = nsp AND
     relname LIKE ptrn
   LOOP
     EXECUTE 'GRANT ' || prv || ' ON ' || nsp || '.' || obj.relname || ' TO ' || usr;
     num := num + 1;
   END LOOP;
   RETURN num;
 END;
 $$;
 H   DROP FUNCTION public.pg_grant(usr text, prv text, ptrn text, nsp text);
       public       postgres    false    771    6            �	           0    0 :   FUNCTION pg_grant(usr text, prv text, ptrn text, nsp text)    COMMENT     �  COMMENT ON FUNCTION pg_grant(usr text, prv text, ptrn text, nsp text) IS 'Grants privileges on database or schema objects in bulk. Parameters are the database user or role, 
 the privilege or (comma-separated) privileges to grant, the text pattern (for LIKE queries) to 
 match schema  objects by, and the name of the schema (public for the default public schema). 
 Returns the number of schema objects to which the privilege(s) were granted.';
            public       postgres    false    251            �            1255    16543     pg_owner(text, text, text, text)    FUNCTION     �  CREATE FUNCTION pg_owner(curr_owner text, new_owner text, ptrn text, nsp text) RETURNS integer
    LANGUAGE plpgsql
    AS $$ DECLARE
   obj record;
   num integer;
 BEGIN
   num:=0;
   FOR obj IN SELECT relname FROM pg_class c
     JOIN pg_namespace ns ON (c.relnamespace = ns.oid)
     JOIN pg_roles u ON (u.oid = c.relowner)
     WHERE relkind IN ('r','v','S') 
     AND nspname = nsp AND relname LIKE ptrn
     AND u.rolname = COALESCE(curr_owner, u.rolname)
     ORDER BY relkind DESC
   LOOP
     EXECUTE 'ALTER TABLE ' || nsp || '.' || obj.relname || ' OWNER TO ' || new_owner;
     num := num + 1;
   END LOOP;
   RETURN num;
 END;
 $$;
 U   DROP FUNCTION public.pg_owner(curr_owner text, new_owner text, ptrn text, nsp text);
       public       postgres    false    771    6            �	           0    0 G   FUNCTION pg_owner(curr_owner text, new_owner text, ptrn text, nsp text)    COMMENT     �  COMMENT ON FUNCTION pg_owner(curr_owner text, new_owner text, ptrn text, nsp text) IS 'Changes the owner on database or schema objects in bulk. Parameters are the current database owner (or role), the new database owner (or role), 
 the text pattern (for LIKE queries) to match schema  objects by, and the name of the schema (public for the default public schema). 
 Returns the number of schema objects for which the owner was changed.';
            public       postgres    false    252            �            1259    16544 
   auth_group    TABLE     ^   CREATE TABLE auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);
    DROP TABLE public.auth_group;
       public         feeding_app    false    6            �	           0    0 
   auth_group    ACL     �   REVOKE ALL ON TABLE auth_group FROM PUBLIC;
REVOKE ALL ON TABLE auth_group FROM feeding_app;
GRANT ALL ON TABLE auth_group TO feeding_app;
            public       feeding_app    false    140            �            1259    16547    auth_group_id_seq    SEQUENCE     s   CREATE SEQUENCE auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
 (   DROP SEQUENCE public.auth_group_id_seq;
       public       feeding_app    false    140    6            �	           0    0    auth_group_id_seq    SEQUENCE OWNED BY     9   ALTER SEQUENCE auth_group_id_seq OWNED BY auth_group.id;
            public       feeding_app    false    141            �	           0    0    auth_group_id_seq    SEQUENCE SET     8   SELECT pg_catalog.setval('auth_group_id_seq', 3, true);
            public       feeding_app    false    141            �	           0    0    auth_group_id_seq    ACL     �   REVOKE ALL ON SEQUENCE auth_group_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE auth_group_id_seq FROM feeding_app;
GRANT ALL ON SEQUENCE auth_group_id_seq TO feeding_app;
            public       feeding_app    false    141            �            1259    16549    auth_group_permissions    TABLE     �   CREATE TABLE auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);
 *   DROP TABLE public.auth_group_permissions;
       public         feeding_app    false    6            �	           0    0    auth_group_permissions    ACL     �   REVOKE ALL ON TABLE auth_group_permissions FROM PUBLIC;
REVOKE ALL ON TABLE auth_group_permissions FROM feeding_app;
GRANT ALL ON TABLE auth_group_permissions TO feeding_app;
            public       feeding_app    false    142            �            1259    16552    auth_group_permissions_id_seq    SEQUENCE        CREATE SEQUENCE auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
 4   DROP SEQUENCE public.auth_group_permissions_id_seq;
       public       feeding_app    false    142    6            �	           0    0    auth_group_permissions_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE auth_group_permissions_id_seq OWNED BY auth_group_permissions.id;
            public       feeding_app    false    143            �	           0    0    auth_group_permissions_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('auth_group_permissions_id_seq', 335, true);
            public       feeding_app    false    143            �	           0    0    auth_group_permissions_id_seq    ACL     �   REVOKE ALL ON SEQUENCE auth_group_permissions_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE auth_group_permissions_id_seq FROM feeding_app;
GRANT ALL ON SEQUENCE auth_group_permissions_id_seq TO feeding_app;
            public       feeding_app    false    143            �            1259    16554    auth_message    TABLE     p   CREATE TABLE auth_message (
    id integer NOT NULL,
    user_id integer NOT NULL,
    message text NOT NULL
);
     DROP TABLE public.auth_message;
       public         feeding_app    false    6            �	           0    0    auth_message    ACL     �   REVOKE ALL ON TABLE auth_message FROM PUBLIC;
REVOKE ALL ON TABLE auth_message FROM feeding_app;
GRANT ALL ON TABLE auth_message TO feeding_app;
            public       feeding_app    false    144            �            1259    16560    auth_message_id_seq    SEQUENCE     u   CREATE SEQUENCE auth_message_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
 *   DROP SEQUENCE public.auth_message_id_seq;
       public       feeding_app    false    144    6            �	           0    0    auth_message_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE auth_message_id_seq OWNED BY auth_message.id;
            public       feeding_app    false    145            �	           0    0    auth_message_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('auth_message_id_seq', 3077, true);
            public       feeding_app    false    145            �	           0    0    auth_message_id_seq    ACL     �   REVOKE ALL ON SEQUENCE auth_message_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE auth_message_id_seq FROM feeding_app;
GRANT ALL ON SEQUENCE auth_message_id_seq TO feeding_app;
            public       feeding_app    false    145            �            1259    16562    auth_permission    TABLE     �   CREATE TABLE auth_permission (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);
 #   DROP TABLE public.auth_permission;
       public         feeding_app    false    6            �	           0    0    auth_permission    ACL     �   REVOKE ALL ON TABLE auth_permission FROM PUBLIC;
REVOKE ALL ON TABLE auth_permission FROM feeding_app;
GRANT ALL ON TABLE auth_permission TO feeding_app;
            public       feeding_app    false    146            �            1259    16565    auth_permission_id_seq    SEQUENCE     x   CREATE SEQUENCE auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
 -   DROP SEQUENCE public.auth_permission_id_seq;
       public       feeding_app    false    6    146            �	           0    0    auth_permission_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE auth_permission_id_seq OWNED BY auth_permission.id;
            public       feeding_app    false    147            �	           0    0    auth_permission_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('auth_permission_id_seq', 189, true);
            public       feeding_app    false    147            �	           0    0    auth_permission_id_seq    ACL     �   REVOKE ALL ON SEQUENCE auth_permission_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE auth_permission_id_seq FROM feeding_app;
GRANT ALL ON SEQUENCE auth_permission_id_seq TO feeding_app;
            public       feeding_app    false    147            �            1259    16567 	   auth_user    TABLE     �  CREATE TABLE auth_user (
    id integer NOT NULL,
    username character varying(30) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(75) NOT NULL,
    password character varying(128) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    is_superuser boolean NOT NULL,
    last_login timestamp with time zone NOT NULL,
    date_joined timestamp with time zone NOT NULL
);
    DROP TABLE public.auth_user;
       public         feeding_app    false    6            �	           0    0 	   auth_user    ACL     �   REVOKE ALL ON TABLE auth_user FROM PUBLIC;
REVOKE ALL ON TABLE auth_user FROM feeding_app;
GRANT ALL ON TABLE auth_user TO feeding_app;
            public       feeding_app    false    148            �            1259    16570    auth_user_groups    TABLE     x   CREATE TABLE auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);
 $   DROP TABLE public.auth_user_groups;
       public         feeding_app    false    6            �	           0    0    auth_user_groups    ACL     �   REVOKE ALL ON TABLE auth_user_groups FROM PUBLIC;
REVOKE ALL ON TABLE auth_user_groups FROM feeding_app;
GRANT ALL ON TABLE auth_user_groups TO feeding_app;
            public       feeding_app    false    149            �            1259    16573    auth_user_groups_id_seq    SEQUENCE     y   CREATE SEQUENCE auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
 .   DROP SEQUENCE public.auth_user_groups_id_seq;
       public       feeding_app    false    149    6            �	           0    0    auth_user_groups_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE auth_user_groups_id_seq OWNED BY auth_user_groups.id;
            public       feeding_app    false    150            �	           0    0    auth_user_groups_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('auth_user_groups_id_seq', 96, true);
            public       feeding_app    false    150            �	           0    0    auth_user_groups_id_seq    ACL     �   REVOKE ALL ON SEQUENCE auth_user_groups_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE auth_user_groups_id_seq FROM feeding_app;
GRANT ALL ON SEQUENCE auth_user_groups_id_seq TO feeding_app;
            public       feeding_app    false    150            �            1259    16575    auth_user_id_seq    SEQUENCE     r   CREATE SEQUENCE auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
 '   DROP SEQUENCE public.auth_user_id_seq;
       public       feeding_app    false    6    148            �	           0    0    auth_user_id_seq    SEQUENCE OWNED BY     7   ALTER SEQUENCE auth_user_id_seq OWNED BY auth_user.id;
            public       feeding_app    false    151            �	           0    0    auth_user_id_seq    SEQUENCE SET     8   SELECT pg_catalog.setval('auth_user_id_seq', 37, true);
            public       feeding_app    false    151            �	           0    0    auth_user_id_seq    ACL     �   REVOKE ALL ON SEQUENCE auth_user_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE auth_user_id_seq FROM feeding_app;
GRANT ALL ON SEQUENCE auth_user_id_seq TO feeding_app;
            public       feeding_app    false    151            �            1259    16577    auth_user_user_permissions    TABLE     �   CREATE TABLE auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);
 .   DROP TABLE public.auth_user_user_permissions;
       public         feeding_app    false    6            �	           0    0    auth_user_user_permissions    ACL     �   REVOKE ALL ON TABLE auth_user_user_permissions FROM PUBLIC;
REVOKE ALL ON TABLE auth_user_user_permissions FROM feeding_app;
GRANT ALL ON TABLE auth_user_user_permissions TO feeding_app;
            public       feeding_app    false    152            �            1259    16580 !   auth_user_user_permissions_id_seq    SEQUENCE     �   CREATE SEQUENCE auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
 8   DROP SEQUENCE public.auth_user_user_permissions_id_seq;
       public       feeding_app    false    152    6            �	           0    0 !   auth_user_user_permissions_id_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE auth_user_user_permissions_id_seq OWNED BY auth_user_user_permissions.id;
            public       feeding_app    false    153            �	           0    0 !   auth_user_user_permissions_id_seq    SEQUENCE SET     K   SELECT pg_catalog.setval('auth_user_user_permissions_id_seq', 1377, true);
            public       feeding_app    false    153            �	           0    0 !   auth_user_user_permissions_id_seq    ACL     �   REVOKE ALL ON SEQUENCE auth_user_user_permissions_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE auth_user_user_permissions_id_seq FROM feeding_app;
GRANT ALL ON SEQUENCE auth_user_user_permissions_id_seq TO feeding_app;
            public       feeding_app    false    153            �            1259    16582    django_admin_log    TABLE     �  CREATE TABLE django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    user_id integer NOT NULL,
    content_type_id integer,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);
 $   DROP TABLE public.django_admin_log;
       public         feeding_app    false    2110    6            �	           0    0    django_admin_log    ACL     �   REVOKE ALL ON TABLE django_admin_log FROM PUBLIC;
REVOKE ALL ON TABLE django_admin_log FROM feeding_app;
GRANT ALL ON TABLE django_admin_log TO feeding_app;
            public       feeding_app    false    154            �            1259    16589    django_admin_log_id_seq    SEQUENCE     y   CREATE SEQUENCE django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
 .   DROP SEQUENCE public.django_admin_log_id_seq;
       public       feeding_app    false    154    6            �	           0    0    django_admin_log_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE django_admin_log_id_seq OWNED BY django_admin_log.id;
            public       feeding_app    false    155            �	           0    0    django_admin_log_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('django_admin_log_id_seq', 2727, true);
            public       feeding_app    false    155            �	           0    0    django_admin_log_id_seq    ACL     �   REVOKE ALL ON SEQUENCE django_admin_log_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE django_admin_log_id_seq FROM feeding_app;
GRANT ALL ON SEQUENCE django_admin_log_id_seq TO feeding_app;
            public       feeding_app    false    155            �            1259    16591    django_content_type    TABLE     �   CREATE TABLE django_content_type (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);
 '   DROP TABLE public.django_content_type;
       public         feeding_app    false    6            �	           0    0    django_content_type    ACL     �   REVOKE ALL ON TABLE django_content_type FROM PUBLIC;
REVOKE ALL ON TABLE django_content_type FROM feeding_app;
GRANT ALL ON TABLE django_content_type TO feeding_app;
            public       feeding_app    false    156            �            1259    16594    django_content_type_id_seq    SEQUENCE     |   CREATE SEQUENCE django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
 1   DROP SEQUENCE public.django_content_type_id_seq;
       public       feeding_app    false    6    156            �	           0    0    django_content_type_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE django_content_type_id_seq OWNED BY django_content_type.id;
            public       feeding_app    false    157            �	           0    0    django_content_type_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('django_content_type_id_seq', 63, true);
            public       feeding_app    false    157             
           0    0    django_content_type_id_seq    ACL     �   REVOKE ALL ON SEQUENCE django_content_type_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE django_content_type_id_seq FROM feeding_app;
GRANT ALL ON SEQUENCE django_content_type_id_seq TO feeding_app;
            public       feeding_app    false    157            �            1259    16596    django_session    TABLE     �   CREATE TABLE django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);
 "   DROP TABLE public.django_session;
       public         feeding_app    false    6            
           0    0    django_session    ACL     �   REVOKE ALL ON TABLE django_session FROM PUBLIC;
REVOKE ALL ON TABLE django_session FROM feeding_app;
GRANT ALL ON TABLE django_session TO feeding_app;
            public       feeding_app    false    158            �            1259    16602    django_site    TABLE     �   CREATE TABLE django_site (
    id integer NOT NULL,
    domain character varying(100) NOT NULL,
    name character varying(50) NOT NULL
);
    DROP TABLE public.django_site;
       public         feeding_app    false    6            
           0    0    django_site    ACL     �   REVOKE ALL ON TABLE django_site FROM PUBLIC;
REVOKE ALL ON TABLE django_site FROM feeding_app;
GRANT ALL ON TABLE django_site TO feeding_app;
            public       feeding_app    false    159            �            1259    16605    django_site_id_seq    SEQUENCE     t   CREATE SEQUENCE django_site_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
 )   DROP SEQUENCE public.django_site_id_seq;
       public       feeding_app    false    159    6            
           0    0    django_site_id_seq    SEQUENCE OWNED BY     ;   ALTER SEQUENCE django_site_id_seq OWNED BY django_site.id;
            public       feeding_app    false    160            
           0    0    django_site_id_seq    SEQUENCE SET     9   SELECT pg_catalog.setval('django_site_id_seq', 1, true);
            public       feeding_app    false    160            
           0    0    django_site_id_seq    ACL     �   REVOKE ALL ON SEQUENCE django_site_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE django_site_id_seq FROM feeding_app;
GRANT ALL ON SEQUENCE django_site_id_seq TO feeding_app;
            public       feeding_app    false    160            �            1259    16607    explorer_bucket    TABLE     �   CREATE TABLE explorer_bucket (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    title character varying(255) NOT NULL,
    description text
);
 #   DROP TABLE public.explorer_bucket;
       public         feeding_app    false    6            �            1259    16613    explorer_bucket_id_seq    SEQUENCE     x   CREATE SEQUENCE explorer_bucket_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
 -   DROP SEQUENCE public.explorer_bucket_id_seq;
       public       feeding_app    false    6    161            
           0    0    explorer_bucket_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE explorer_bucket_id_seq OWNED BY explorer_bucket.id;
            public       feeding_app    false    162            
           0    0    explorer_bucket_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('explorer_bucket_id_seq', 36, true);
            public       feeding_app    false    162            �            1259    16615    explorer_trialinbucket    TABLE     }   CREATE TABLE explorer_trialinbucket (
    id integer NOT NULL,
    trial_id integer NOT NULL,
    bin_id integer NOT NULL
);
 *   DROP TABLE public.explorer_trialinbucket;
       public         feeding_app    false    6            �            1259    16618    explorer_trialinbucket_id_seq    SEQUENCE        CREATE SEQUENCE explorer_trialinbucket_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
 4   DROP SEQUENCE public.explorer_trialinbucket_id_seq;
       public       feeding_app    false    6    163            
           0    0    explorer_trialinbucket_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE explorer_trialinbucket_id_seq OWNED BY explorer_trialinbucket.id;
            public       feeding_app    false    164            	
           0    0    explorer_trialinbucket_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('explorer_trialinbucket_id_seq', 310, true);
            public       feeding_app    false    164            �            1259    16620    feed_ageunit    TABLE     �   CREATE TABLE feed_ageunit (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    label character varying(255) NOT NULL
);
     DROP TABLE public.feed_ageunit;
       public         feeding_app    false    6            �            1259    16623    feed_ageunit_id_seq    SEQUENCE     u   CREATE SEQUENCE feed_ageunit_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
 *   DROP SEQUENCE public.feed_ageunit_id_seq;
       public       feeding_app    false    165    6            

           0    0    feed_ageunit_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE feed_ageunit_id_seq OWNED BY feed_ageunit.id;
            public       feeding_app    false    166            
           0    0    feed_ageunit_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('feed_ageunit_id_seq', 4, true);
            public       feeding_app    false    166            �            1259    16625    feed_anatomicallocation    TABLE       CREATE TABLE feed_anatomicallocation (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    label character varying(255) NOT NULL,
    category integer NOT NULL
);
 +   DROP TABLE public.feed_anatomicallocation;
       public         feeding_app    false    6            �            1259    16628    feed_anatomicallocation_id_seq    SEQUENCE     �   CREATE SEQUENCE feed_anatomicallocation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
 5   DROP SEQUENCE public.feed_anatomicallocation_id_seq;
       public       feeding_app    false    167    6            
           0    0    feed_anatomicallocation_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE feed_anatomicallocation_id_seq OWNED BY feed_anatomicallocation.id;
            public       feeding_app    false    168            
           0    0    feed_anatomicallocation_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('feed_anatomicallocation_id_seq', 54, true);
            public       feeding_app    false    168            �            1259    16630    feed_anteriorposterioraxis    TABLE     �   CREATE TABLE feed_anteriorposterioraxis (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    label character varying(255) NOT NULL
);
 .   DROP TABLE public.feed_anteriorposterioraxis;
       public         feeding_app    false    6            
           0    0    feed_anteriorposterioraxis    ACL     �   REVOKE ALL ON TABLE feed_anteriorposterioraxis FROM PUBLIC;
REVOKE ALL ON TABLE feed_anteriorposterioraxis FROM feeding_app;
GRANT ALL ON TABLE feed_anteriorposterioraxis TO feeding_app;
            public       feeding_app    false    169            �            1259    16633 !   feed_anteriorposterioraxis_id_seq    SEQUENCE     �   CREATE SEQUENCE feed_anteriorposterioraxis_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
 8   DROP SEQUENCE public.feed_anteriorposterioraxis_id_seq;
       public       feeding_app    false    6    169            
           0    0 !   feed_anteriorposterioraxis_id_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE feed_anteriorposterioraxis_id_seq OWNED BY feed_anteriorposterioraxis.id;
            public       feeding_app    false    170            
           0    0 !   feed_anteriorposterioraxis_id_seq    SEQUENCE SET     H   SELECT pg_catalog.setval('feed_anteriorposterioraxis_id_seq', 3, true);
            public       feeding_app    false    170            
           0    0 !   feed_anteriorposterioraxis_id_seq    ACL     �   REVOKE ALL ON SEQUENCE feed_anteriorposterioraxis_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE feed_anteriorposterioraxis_id_seq FROM feeding_app;
GRANT ALL ON SEQUENCE feed_anteriorposterioraxis_id_seq TO feeding_app;
            public       feeding_app    false    170            �            1259    16635    feed_behavior    TABLE     �   CREATE TABLE feed_behavior (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    label character varying(255) NOT NULL
);
 !   DROP TABLE public.feed_behavior;
       public         feeding_app    false    6            
           0    0    feed_behavior    ACL     �   REVOKE ALL ON TABLE feed_behavior FROM PUBLIC;
REVOKE ALL ON TABLE feed_behavior FROM feeding_app;
GRANT ALL ON TABLE feed_behavior TO feeding_app;
            public       feeding_app    false    171            �            1259    16638    feed_behavior_id_seq    SEQUENCE     v   CREATE SEQUENCE feed_behavior_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
 +   DROP SEQUENCE public.feed_behavior_id_seq;
       public       feeding_app    false    171    6            
           0    0    feed_behavior_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE feed_behavior_id_seq OWNED BY feed_behavior.id;
            public       feeding_app    false    172            
           0    0    feed_behavior_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('feed_behavior_id_seq', 14, true);
            public       feeding_app    false    172            
           0    0    feed_behavior_id_seq    ACL     �   REVOKE ALL ON SEQUENCE feed_behavior_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE feed_behavior_id_seq FROM feeding_app;
GRANT ALL ON SEQUENCE feed_behavior_id_seq TO feeding_app;
            public       feeding_app    false    172            �            1259    16640    feed_channel    TABLE     *  CREATE TABLE feed_channel (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    setup_id integer NOT NULL,
    name character varying(255) NOT NULL,
    rate integer NOT NULL,
    notes text
);
     DROP TABLE public.feed_channel;
       public         feeding_app    false    6            
           0    0    feed_channel    ACL     �   REVOKE ALL ON TABLE feed_channel FROM PUBLIC;
REVOKE ALL ON TABLE feed_channel FROM feeding_app;
GRANT ALL ON TABLE feed_channel TO feeding_app;
            public       feeding_app    false    173            �            1259    16646    feed_channel_id_seq    SEQUENCE     u   CREATE SEQUENCE feed_channel_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
 *   DROP SEQUENCE public.feed_channel_id_seq;
       public       feeding_app    false    173    6            
           0    0    feed_channel_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE feed_channel_id_seq OWNED BY feed_channel.id;
            public       feeding_app    false    174            
           0    0    feed_channel_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('feed_channel_id_seq', 1396, true);
            public       feeding_app    false    174            
           0    0    feed_channel_id_seq    ACL     �   REVOKE ALL ON SEQUENCE feed_channel_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE feed_channel_id_seq FROM feeding_app;
GRANT ALL ON SEQUENCE feed_channel_id_seq TO feeding_app;
            public       feeding_app    false    174            �            1259    16648    feed_channellineup    TABLE       CREATE TABLE feed_channellineup (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    session_id integer NOT NULL,
    channel_id integer,
    "position" integer NOT NULL
);
 &   DROP TABLE public.feed_channellineup;
       public         feeding_app    false    6            
           0    0    feed_channellineup    ACL     �   REVOKE ALL ON TABLE feed_channellineup FROM PUBLIC;
REVOKE ALL ON TABLE feed_channellineup FROM feeding_app;
GRANT ALL ON TABLE feed_channellineup TO feeding_app;
            public       feeding_app    false    175            �            1259    16651    feed_channellineup_id_seq    SEQUENCE     {   CREATE SEQUENCE feed_channellineup_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
 0   DROP SEQUENCE public.feed_channellineup_id_seq;
       public       feeding_app    false    175    6            
           0    0    feed_channellineup_id_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE feed_channellineup_id_seq OWNED BY feed_channellineup.id;
            public       feeding_app    false    176            
           0    0    feed_channellineup_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('feed_channellineup_id_seq', 1197, true);
            public       feeding_app    false    176            
           0    0    feed_channellineup_id_seq    ACL     �   REVOKE ALL ON SEQUENCE feed_channellineup_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE feed_channellineup_id_seq FROM feeding_app;
GRANT ALL ON SEQUENCE feed_channellineup_id_seq TO feeding_app;
            public       feeding_app    false    176            �            1259    16653    feed_depthaxis    TABLE     �   CREATE TABLE feed_depthaxis (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    label character varying(255) NOT NULL
);
 "   DROP TABLE public.feed_depthaxis;
       public         feeding_app    false    6            
           0    0    feed_depthaxis    ACL     �   REVOKE ALL ON TABLE feed_depthaxis FROM PUBLIC;
REVOKE ALL ON TABLE feed_depthaxis FROM feeding_app;
GRANT ALL ON TABLE feed_depthaxis TO feeding_app;
            public       feeding_app    false    177            �            1259    16656    feed_depthaxis_id_seq    SEQUENCE     w   CREATE SEQUENCE feed_depthaxis_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
 ,   DROP SEQUENCE public.feed_depthaxis_id_seq;
       public       feeding_app    false    6    177            
           0    0    feed_depthaxis_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE feed_depthaxis_id_seq OWNED BY feed_depthaxis.id;
            public       feeding_app    false    178             
           0    0    feed_depthaxis_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('feed_depthaxis_id_seq', 2, true);
            public       feeding_app    false    178            !
           0    0    feed_depthaxis_id_seq    ACL     �   REVOKE ALL ON SEQUENCE feed_depthaxis_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE feed_depthaxis_id_seq FROM feeding_app;
GRANT ALL ON SEQUENCE feed_depthaxis_id_seq TO feeding_app;
            public       feeding_app    false    178            �            1259    16658    feed_developmentstage    TABLE     �   CREATE TABLE feed_developmentstage (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    label character varying(255) NOT NULL
);
 )   DROP TABLE public.feed_developmentstage;
       public         feeding_app    false    6            "
           0    0    feed_developmentstage    ACL     �   REVOKE ALL ON TABLE feed_developmentstage FROM PUBLIC;
REVOKE ALL ON TABLE feed_developmentstage FROM feeding_app;
GRANT ALL ON TABLE feed_developmentstage TO feeding_app;
            public       feeding_app    false    179            �            1259    16661    feed_developmentstage_id_seq    SEQUENCE     ~   CREATE SEQUENCE feed_developmentstage_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
 3   DROP SEQUENCE public.feed_developmentstage_id_seq;
       public       feeding_app    false    6    179            #
           0    0    feed_developmentstage_id_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE feed_developmentstage_id_seq OWNED BY feed_developmentstage.id;
            public       feeding_app    false    180            $
           0    0    feed_developmentstage_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('feed_developmentstage_id_seq', 6, true);
            public       feeding_app    false    180            %
           0    0    feed_developmentstage_id_seq    ACL     �   REVOKE ALL ON SEQUENCE feed_developmentstage_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE feed_developmentstage_id_seq FROM feeding_app;
GRANT ALL ON SEQUENCE feed_developmentstage_id_seq TO feeding_app;
            public       feeding_app    false    180            �            1259    16663    feed_dorsalventralaxis    TABLE     �   CREATE TABLE feed_dorsalventralaxis (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    label character varying(255) NOT NULL
);
 *   DROP TABLE public.feed_dorsalventralaxis;
       public         feeding_app    false    6            &
           0    0    feed_dorsalventralaxis    ACL     �   REVOKE ALL ON TABLE feed_dorsalventralaxis FROM PUBLIC;
REVOKE ALL ON TABLE feed_dorsalventralaxis FROM feeding_app;
GRANT ALL ON TABLE feed_dorsalventralaxis TO feeding_app;
            public       feeding_app    false    181            �            1259    16666    feed_dorsalventralaxis_id_seq    SEQUENCE        CREATE SEQUENCE feed_dorsalventralaxis_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
 4   DROP SEQUENCE public.feed_dorsalventralaxis_id_seq;
       public       feeding_app    false    181    6            '
           0    0    feed_dorsalventralaxis_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE feed_dorsalventralaxis_id_seq OWNED BY feed_dorsalventralaxis.id;
            public       feeding_app    false    182            (
           0    0    feed_dorsalventralaxis_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('feed_dorsalventralaxis_id_seq', 2, true);
            public       feeding_app    false    182            )
           0    0    feed_dorsalventralaxis_id_seq    ACL     �   REVOKE ALL ON SEQUENCE feed_dorsalventralaxis_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE feed_dorsalventralaxis_id_seq FROM feeding_app;
GRANT ALL ON SEQUENCE feed_dorsalventralaxis_id_seq TO feeding_app;
            public       feeding_app    false    182            �            1259    16668    feed_electrodetype    TABLE     �   CREATE TABLE feed_electrodetype (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    label character varying(255) NOT NULL
);
 &   DROP TABLE public.feed_electrodetype;
       public         feeding_app    false    6            *
           0    0    feed_electrodetype    ACL     �   REVOKE ALL ON TABLE feed_electrodetype FROM PUBLIC;
REVOKE ALL ON TABLE feed_electrodetype FROM feeding_app;
GRANT ALL ON TABLE feed_electrodetype TO feeding_app;
            public       feeding_app    false    183            �            1259    16671    feed_eletrodetype_id_seq    SEQUENCE     z   CREATE SEQUENCE feed_eletrodetype_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
 /   DROP SEQUENCE public.feed_eletrodetype_id_seq;
       public       feeding_app    false    183    6            +
           0    0    feed_eletrodetype_id_seq    SEQUENCE OWNED BY     H   ALTER SEQUENCE feed_eletrodetype_id_seq OWNED BY feed_electrodetype.id;
            public       feeding_app    false    184            ,
           0    0    feed_eletrodetype_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('feed_eletrodetype_id_seq', 5, true);
            public       feeding_app    false    184            -
           0    0    feed_eletrodetype_id_seq    ACL     �   REVOKE ALL ON SEQUENCE feed_eletrodetype_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE feed_eletrodetype_id_seq FROM feeding_app;
GRANT ALL ON SEQUENCE feed_eletrodetype_id_seq TO feeding_app;
            public       feeding_app    false    184            �            1259    16673    feed_emgchannel    TABLE     �   CREATE TABLE feed_emgchannel (
    channel_ptr_id integer NOT NULL,
    sensor_id integer NOT NULL,
    emg_filtering_id integer NOT NULL,
    emg_amplification integer,
    unit_id integer NOT NULL
);
 #   DROP TABLE public.feed_emgchannel;
       public         feeding_app    false    6            .
           0    0    feed_emgchannel    ACL     �   REVOKE ALL ON TABLE feed_emgchannel FROM PUBLIC;
REVOKE ALL ON TABLE feed_emgchannel FROM feeding_app;
GRANT ALL ON TABLE feed_emgchannel TO feeding_app;
            public       feeding_app    false    185            �            1259    16676    feed_emgfiltering    TABLE     �   CREATE TABLE feed_emgfiltering (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    label character varying(255) NOT NULL
);
 %   DROP TABLE public.feed_emgfiltering;
       public         feeding_app    false    6            /
           0    0    feed_emgfiltering    ACL     �   REVOKE ALL ON TABLE feed_emgfiltering FROM PUBLIC;
REVOKE ALL ON TABLE feed_emgfiltering FROM feeding_app;
GRANT ALL ON TABLE feed_emgfiltering TO feeding_app;
            public       feeding_app    false    186            �            1259    16679    feed_emgfiltering_id_seq    SEQUENCE     z   CREATE SEQUENCE feed_emgfiltering_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
 /   DROP SEQUENCE public.feed_emgfiltering_id_seq;
       public       feeding_app    false    186    6            0
           0    0    feed_emgfiltering_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE feed_emgfiltering_id_seq OWNED BY feed_emgfiltering.id;
            public       feeding_app    false    187            1
           0    0    feed_emgfiltering_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('feed_emgfiltering_id_seq', 7, true);
            public       feeding_app    false    187            2
           0    0    feed_emgfiltering_id_seq    ACL     �   REVOKE ALL ON SEQUENCE feed_emgfiltering_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE feed_emgfiltering_id_seq FROM feeding_app;
GRANT ALL ON SEQUENCE feed_emgfiltering_id_seq TO feeding_app;
            public       feeding_app    false    187            �            1259    16681    feed_emgsensor    TABLE     �   CREATE TABLE feed_emgsensor (
    sensor_ptr_id integer NOT NULL,
    axisdepth_id integer,
    electrode_type_id integer,
    location_controlled_id integer NOT NULL
);
 "   DROP TABLE public.feed_emgsensor;
       public         feeding_app    false    6            3
           0    0    feed_emgsensor    ACL     �   REVOKE ALL ON TABLE feed_emgsensor FROM PUBLIC;
REVOKE ALL ON TABLE feed_emgsensor FROM feeding_app;
GRANT ALL ON TABLE feed_emgsensor TO feeding_app;
            public       feeding_app    false    188            �            1259    16684    feed_emgsetup    TABLE     k   CREATE TABLE feed_emgsetup (
    setup_ptr_id integer NOT NULL,
    preamplifier character varying(255)
);
 !   DROP TABLE public.feed_emgsetup;
       public         feeding_app    false    6            4
           0    0    feed_emgsetup    ACL     �   REVOKE ALL ON TABLE feed_emgsetup FROM PUBLIC;
REVOKE ALL ON TABLE feed_emgsetup FROM feeding_app;
GRANT ALL ON TABLE feed_emgsetup TO feeding_app;
            public       feeding_app    false    189            �            1259    16687    feed_eventchannel    TABLE     i   CREATE TABLE feed_eventchannel (
    channel_ptr_id integer NOT NULL,
    unit character varying(255)
);
 %   DROP TABLE public.feed_eventchannel;
       public         feeding_app    false    6            �            1259    16690    feed_eventsetup    TABLE     D   CREATE TABLE feed_eventsetup (
    setup_ptr_id integer NOT NULL
);
 #   DROP TABLE public.feed_eventsetup;
       public         feeding_app    false    6            �            1259    16693    feed_experiment    TABLE     �  CREATE TABLE feed_experiment (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    study_id integer NOT NULL,
    subject_id integer NOT NULL,
    accession character varying(255),
    start timestamp with time zone,
    "end" timestamp with time zone,
    bookkeeping character varying(255),
    description text,
    subj_devstage_id integer NOT NULL,
    subj_age numeric(19,5),
    subj_weight numeric(19,5),
    subj_tooth character varying(255),
    subject_notes text,
    impl_notes text,
    title character varying(255) DEFAULT 'new Experiment - edit this'::character varying NOT NULL,
    subj_ageunit_id integer
);
 #   DROP TABLE public.feed_experiment;
       public         feeding_app    false    2126    6            5
           0    0    feed_experiment    ACL     �   REVOKE ALL ON TABLE feed_experiment FROM PUBLIC;
REVOKE ALL ON TABLE feed_experiment FROM feeding_app;
GRANT ALL ON TABLE feed_experiment TO feeding_app;
            public       feeding_app    false    192            �            1259    16700    feed_experiment_id_seq    SEQUENCE     x   CREATE SEQUENCE feed_experiment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
 -   DROP SEQUENCE public.feed_experiment_id_seq;
       public       feeding_app    false    6    192            6
           0    0    feed_experiment_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE feed_experiment_id_seq OWNED BY feed_experiment.id;
            public       feeding_app    false    193            7
           0    0    feed_experiment_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('feed_experiment_id_seq', 196, true);
            public       feeding_app    false    193            8
           0    0    feed_experiment_id_seq    ACL     �   REVOKE ALL ON SEQUENCE feed_experiment_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE feed_experiment_id_seq FROM feeding_app;
GRANT ALL ON SEQUENCE feed_experiment_id_seq TO feeding_app;
            public       feeding_app    false    193            �            1259    16702    feed_forcechannel    TABLE     }   CREATE TABLE feed_forcechannel (
    channel_ptr_id integer NOT NULL,
    unit_id integer,
    sensor_id integer NOT NULL
);
 %   DROP TABLE public.feed_forcechannel;
       public         feeding_app    false    6            �            1259    16705    feed_forcesensor    TABLE     F   CREATE TABLE feed_forcesensor (
    sensor_ptr_id integer NOT NULL
);
 $   DROP TABLE public.feed_forcesensor;
       public         feeding_app    false    6            �            1259    16708    feed_forcesetup    TABLE     D   CREATE TABLE feed_forcesetup (
    setup_ptr_id integer NOT NULL
);
 #   DROP TABLE public.feed_forcesetup;
       public         feeding_app    false    6            �            1259    16711    feed_illustration    TABLE     8  CREATE TABLE feed_illustration (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    picture character varying(100),
    notes text,
    subject_id integer,
    setup_id integer,
    experiment_id integer
);
 %   DROP TABLE public.feed_illustration;
       public         feeding_app    false    6            9
           0    0    feed_illustration    ACL     �   REVOKE ALL ON TABLE feed_illustration FROM PUBLIC;
REVOKE ALL ON TABLE feed_illustration FROM feeding_app;
GRANT ALL ON TABLE feed_illustration TO feeding_app;
            public       feeding_app    false    197            �            1259    16717    feed_illustration_id_seq    SEQUENCE     z   CREATE SEQUENCE feed_illustration_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
 /   DROP SEQUENCE public.feed_illustration_id_seq;
       public       feeding_app    false    6    197            :
           0    0    feed_illustration_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE feed_illustration_id_seq OWNED BY feed_illustration.id;
            public       feeding_app    false    198            ;
           0    0    feed_illustration_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('feed_illustration_id_seq', 97, true);
            public       feeding_app    false    198            <
           0    0    feed_illustration_id_seq    ACL     �   REVOKE ALL ON SEQUENCE feed_illustration_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE feed_illustration_id_seq FROM feeding_app;
GRANT ALL ON SEQUENCE feed_illustration_id_seq TO feeding_app;
            public       feeding_app    false    198            �            1259    16719    feed_kinematicschannel    TABLE     �   CREATE TABLE feed_kinematicschannel (
    channel_ptr_id integer NOT NULL,
    unit_id integer,
    sensor_id integer NOT NULL
);
 *   DROP TABLE public.feed_kinematicschannel;
       public         feeding_app    false    6            �            1259    16722    feed_kinematicssensor    TABLE     K   CREATE TABLE feed_kinematicssensor (
    sensor_ptr_id integer NOT NULL
);
 )   DROP TABLE public.feed_kinematicssensor;
       public         feeding_app    false    6            �            1259    16725    feed_kinematicssetup    TABLE     I   CREATE TABLE feed_kinematicssetup (
    setup_ptr_id integer NOT NULL
);
 (   DROP TABLE public.feed_kinematicssetup;
       public         feeding_app    false    6            �            1259    16728    feed_mediallateralaxis    TABLE     �   CREATE TABLE feed_mediallateralaxis (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    label character varying(255) NOT NULL
);
 *   DROP TABLE public.feed_mediallateralaxis;
       public         feeding_app    false    6            �            1259    16731    feed_mediallateralaxis_id_seq    SEQUENCE        CREATE SEQUENCE feed_mediallateralaxis_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
 4   DROP SEQUENCE public.feed_mediallateralaxis_id_seq;
       public       feeding_app    false    202    6            =
           0    0    feed_mediallateralaxis_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE feed_mediallateralaxis_id_seq OWNED BY feed_mediallateralaxis.id;
            public       feeding_app    false    203            >
           0    0    feed_mediallateralaxis_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('feed_mediallateralaxis_id_seq', 2, true);
            public       feeding_app    false    203            �            1259    16733    feed_pressurechannel    TABLE     �   CREATE TABLE feed_pressurechannel (
    channel_ptr_id integer NOT NULL,
    unit_id integer,
    sensor_id integer NOT NULL
);
 (   DROP TABLE public.feed_pressurechannel;
       public         feeding_app    false    6            �            1259    16736    feed_pressuresensor    TABLE     I   CREATE TABLE feed_pressuresensor (
    sensor_ptr_id integer NOT NULL
);
 '   DROP TABLE public.feed_pressuresensor;
       public         feeding_app    false    6            �            1259    16739    feed_pressuresetup    TABLE     G   CREATE TABLE feed_pressuresetup (
    setup_ptr_id integer NOT NULL
);
 &   DROP TABLE public.feed_pressuresetup;
       public         feeding_app    false    6            �            1259    16742    feed_proximaldistalaxis    TABLE     �   CREATE TABLE feed_proximaldistalaxis (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    label character varying(255) NOT NULL
);
 +   DROP TABLE public.feed_proximaldistalaxis;
       public         feeding_app    false    6            �            1259    16745    feed_proximaldistalaxis_id_seq    SEQUENCE     �   CREATE SEQUENCE feed_proximaldistalaxis_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
 5   DROP SEQUENCE public.feed_proximaldistalaxis_id_seq;
       public       feeding_app    false    6    207            ?
           0    0    feed_proximaldistalaxis_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE feed_proximaldistalaxis_id_seq OWNED BY feed_proximaldistalaxis.id;
            public       feeding_app    false    208            @
           0    0    feed_proximaldistalaxis_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('feed_proximaldistalaxis_id_seq', 3, true);
            public       feeding_app    false    208            �            1259    16747    feed_restraint    TABLE     �   CREATE TABLE feed_restraint (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    label character varying(255) NOT NULL
);
 "   DROP TABLE public.feed_restraint;
       public         feeding_app    false    6            A
           0    0    feed_restraint    ACL     �   REVOKE ALL ON TABLE feed_restraint FROM PUBLIC;
REVOKE ALL ON TABLE feed_restraint FROM feeding_app;
GRANT ALL ON TABLE feed_restraint TO feeding_app;
            public       feeding_app    false    209            �            1259    16750    feed_restraint_id_seq    SEQUENCE     w   CREATE SEQUENCE feed_restraint_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
 ,   DROP SEQUENCE public.feed_restraint_id_seq;
       public       feeding_app    false    6    209            B
           0    0    feed_restraint_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE feed_restraint_id_seq OWNED BY feed_restraint.id;
            public       feeding_app    false    210            C
           0    0    feed_restraint_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('feed_restraint_id_seq', 9, true);
            public       feeding_app    false    210            D
           0    0    feed_restraint_id_seq    ACL     �   REVOKE ALL ON SEQUENCE feed_restraint_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE feed_restraint_id_seq FROM feeding_app;
GRANT ALL ON SEQUENCE feed_restraint_id_seq TO feeding_app;
            public       feeding_app    false    210            �            1259    16752    feed_sensor    TABLE     �  CREATE TABLE feed_sensor (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    setup_id integer NOT NULL,
    name character varying(255) NOT NULL,
    notes text,
    loc_side_id integer NOT NULL,
    location_freetext character varying(255),
    loc_ap_id integer,
    loc_ml_id integer,
    loc_pd_id integer,
    loc_dv_id integer
);
    DROP TABLE public.feed_sensor;
       public         feeding_app    false    6            E
           0    0    feed_sensor    ACL     �   REVOKE ALL ON TABLE feed_sensor FROM PUBLIC;
REVOKE ALL ON TABLE feed_sensor FROM feeding_app;
GRANT ALL ON TABLE feed_sensor TO feeding_app;
            public       feeding_app    false    211            �            1259    16758    feed_sensor_id_seq    SEQUENCE     t   CREATE SEQUENCE feed_sensor_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
 )   DROP SEQUENCE public.feed_sensor_id_seq;
       public       feeding_app    false    6    211            F
           0    0    feed_sensor_id_seq    SEQUENCE OWNED BY     ;   ALTER SEQUENCE feed_sensor_id_seq OWNED BY feed_sensor.id;
            public       feeding_app    false    212            G
           0    0    feed_sensor_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('feed_sensor_id_seq', 1458, true);
            public       feeding_app    false    212            H
           0    0    feed_sensor_id_seq    ACL     �   REVOKE ALL ON SEQUENCE feed_sensor_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE feed_sensor_id_seq FROM feeding_app;
GRANT ALL ON SEQUENCE feed_sensor_id_seq TO feeding_app;
            public       feeding_app    false    212            �            1259    16760    feed_session    TABLE     m  CREATE TABLE feed_session (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    experiment_id integer NOT NULL,
    accession character varying(255),
    start timestamp with time zone,
    "end" timestamp with time zone,
    "position" integer NOT NULL,
    bookkeeping character varying(255),
    subj_restraint_id integer NOT NULL,
    subj_anesthesia_sedation character varying(255),
    subj_notes text,
    title character varying(255) DEFAULT 'new Recording Session - edit this'::character varying NOT NULL
);
     DROP TABLE public.feed_session;
       public         feeding_app    false    2133    6            I
           0    0    feed_session    ACL     �   REVOKE ALL ON TABLE feed_session FROM PUBLIC;
REVOKE ALL ON TABLE feed_session FROM feeding_app;
GRANT ALL ON TABLE feed_session TO feeding_app;
            public       feeding_app    false    213            �            1259    16767    feed_session_id_seq    SEQUENCE     u   CREATE SEQUENCE feed_session_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
 *   DROP SEQUENCE public.feed_session_id_seq;
       public       feeding_app    false    213    6            J
           0    0    feed_session_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE feed_session_id_seq OWNED BY feed_session.id;
            public       feeding_app    false    214            K
           0    0    feed_session_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('feed_session_id_seq', 212, true);
            public       feeding_app    false    214            L
           0    0    feed_session_id_seq    ACL     �   REVOKE ALL ON SEQUENCE feed_session_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE feed_session_id_seq FROM feeding_app;
GRANT ALL ON SEQUENCE feed_session_id_seq TO feeding_app;
            public       feeding_app    false    214            �            1259    16769 
   feed_setup    TABLE     #  CREATE TABLE feed_setup (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    experiment_id integer NOT NULL,
    notes text,
    sampling_rate integer,
    technique integer NOT NULL
);
    DROP TABLE public.feed_setup;
       public         feeding_app    false    6            M
           0    0 
   feed_setup    ACL     �   REVOKE ALL ON TABLE feed_setup FROM PUBLIC;
REVOKE ALL ON TABLE feed_setup FROM feeding_app;
GRANT ALL ON TABLE feed_setup TO feeding_app;
            public       feeding_app    false    215            �            1259    16775    feed_setup_id_seq    SEQUENCE     s   CREATE SEQUENCE feed_setup_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
 (   DROP SEQUENCE public.feed_setup_id_seq;
       public       feeding_app    false    6    215            N
           0    0    feed_setup_id_seq    SEQUENCE OWNED BY     9   ALTER SEQUENCE feed_setup_id_seq OWNED BY feed_setup.id;
            public       feeding_app    false    216            O
           0    0    feed_setup_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('feed_setup_id_seq', 484, true);
            public       feeding_app    false    216            P
           0    0    feed_setup_id_seq    ACL     �   REVOKE ALL ON SEQUENCE feed_setup_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE feed_setup_id_seq FROM feeding_app;
GRANT ALL ON SEQUENCE feed_setup_id_seq TO feeding_app;
            public       feeding_app    false    216            �            1259    16777 	   feed_side    TABLE     �   CREATE TABLE feed_side (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    label character varying(255) NOT NULL
);
    DROP TABLE public.feed_side;
       public         feeding_app    false    6            Q
           0    0 	   feed_side    ACL     �   REVOKE ALL ON TABLE feed_side FROM PUBLIC;
REVOKE ALL ON TABLE feed_side FROM feeding_app;
GRANT ALL ON TABLE feed_side TO feeding_app;
            public       feeding_app    false    217            �            1259    16780    feed_side_id_seq    SEQUENCE     r   CREATE SEQUENCE feed_side_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
 '   DROP SEQUENCE public.feed_side_id_seq;
       public       feeding_app    false    217    6            R
           0    0    feed_side_id_seq    SEQUENCE OWNED BY     7   ALTER SEQUENCE feed_side_id_seq OWNED BY feed_side.id;
            public       feeding_app    false    218            S
           0    0    feed_side_id_seq    SEQUENCE SET     7   SELECT pg_catalog.setval('feed_side_id_seq', 6, true);
            public       feeding_app    false    218            T
           0    0    feed_side_id_seq    ACL     �   REVOKE ALL ON SEQUENCE feed_side_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE feed_side_id_seq FROM feeding_app;
GRANT ALL ON SEQUENCE feed_side_id_seq TO feeding_app;
            public       feeding_app    false    218            �            1259    16782    feed_sonochannel    TABLE     �   CREATE TABLE feed_sonochannel (
    channel_ptr_id integer NOT NULL,
    crystal1_id integer NOT NULL,
    crystal2_id integer NOT NULL,
    unit_id integer NOT NULL
);
 $   DROP TABLE public.feed_sonochannel;
       public         feeding_app    false    6            U
           0    0    feed_sonochannel    ACL     �   REVOKE ALL ON TABLE feed_sonochannel FROM PUBLIC;
REVOKE ALL ON TABLE feed_sonochannel FROM feeding_app;
GRANT ALL ON TABLE feed_sonochannel TO feeding_app;
            public       feeding_app    false    219            �            1259    16785    feed_sonosensor    TABLE     �   CREATE TABLE feed_sonosensor (
    sensor_ptr_id integer NOT NULL,
    axisdepth_id integer,
    location_controlled_id integer NOT NULL
);
 #   DROP TABLE public.feed_sonosensor;
       public         feeding_app    false    6            V
           0    0    feed_sonosensor    ACL     �   REVOKE ALL ON TABLE feed_sonosensor FROM PUBLIC;
REVOKE ALL ON TABLE feed_sonosensor FROM feeding_app;
GRANT ALL ON TABLE feed_sonosensor TO feeding_app;
            public       feeding_app    false    220            �            1259    16788    feed_sonosetup    TABLE     n   CREATE TABLE feed_sonosetup (
    setup_ptr_id integer NOT NULL,
    sonomicrometer character varying(255)
);
 "   DROP TABLE public.feed_sonosetup;
       public         feeding_app    false    6            W
           0    0    feed_sonosetup    ACL     �   REVOKE ALL ON TABLE feed_sonosetup FROM PUBLIC;
REVOKE ALL ON TABLE feed_sonosetup FROM feeding_app;
GRANT ALL ON TABLE feed_sonosetup TO feeding_app;
            public       feeding_app    false    221            �            1259    16791    feed_strainchannel    TABLE     ~   CREATE TABLE feed_strainchannel (
    channel_ptr_id integer NOT NULL,
    unit_id integer,
    sensor_id integer NOT NULL
);
 &   DROP TABLE public.feed_strainchannel;
       public         feeding_app    false    6            �            1259    16794    feed_strainsensor    TABLE     G   CREATE TABLE feed_strainsensor (
    sensor_ptr_id integer NOT NULL
);
 %   DROP TABLE public.feed_strainsensor;
       public         feeding_app    false    6            �            1259    16797    feed_strainsetup    TABLE     E   CREATE TABLE feed_strainsetup (
    setup_ptr_id integer NOT NULL
);
 $   DROP TABLE public.feed_strainsetup;
       public         feeding_app    false    6            �            1259    16800 
   feed_study    TABLE     	  CREATE TABLE feed_study (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    accession character varying(255),
    bookkeeping character varying(255),
    start timestamp with time zone NOT NULL,
    "end" timestamp with time zone,
    funding_agency character varying(255),
    approval_secured character varying(255),
    description text NOT NULL,
    title character varying(255) NOT NULL,
    resources text
);
    DROP TABLE public.feed_study;
       public         feeding_app    false    6            X
           0    0 
   feed_study    ACL     �   REVOKE ALL ON TABLE feed_study FROM PUBLIC;
REVOKE ALL ON TABLE feed_study FROM feeding_app;
GRANT ALL ON TABLE feed_study TO feeding_app;
            public       feeding_app    false    225            �            1259    16806    feed_study_id_seq    SEQUENCE     s   CREATE SEQUENCE feed_study_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
 (   DROP SEQUENCE public.feed_study_id_seq;
       public       feeding_app    false    225    6            Y
           0    0    feed_study_id_seq    SEQUENCE OWNED BY     9   ALTER SEQUENCE feed_study_id_seq OWNED BY feed_study.id;
            public       feeding_app    false    226            Z
           0    0    feed_study_id_seq    SEQUENCE SET     9   SELECT pg_catalog.setval('feed_study_id_seq', 81, true);
            public       feeding_app    false    226            [
           0    0    feed_study_id_seq    ACL     �   REVOKE ALL ON SEQUENCE feed_study_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE feed_study_id_seq FROM feeding_app;
GRANT ALL ON SEQUENCE feed_study_id_seq TO feeding_app;
            public       feeding_app    false    226            �            1259    16808    feed_studyprivate    TABLE     �  CREATE TABLE feed_studyprivate (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    study_id integer NOT NULL,
    pi character varying(255) NOT NULL,
    organization character varying(255),
    lab character varying(255),
    funding character varying(255),
    approval character varying(255),
    notes text
);
 %   DROP TABLE public.feed_studyprivate;
       public         feeding_app    false    6            \
           0    0    feed_studyprivate    ACL     �   REVOKE ALL ON TABLE feed_studyprivate FROM PUBLIC;
REVOKE ALL ON TABLE feed_studyprivate FROM feeding_app;
GRANT ALL ON TABLE feed_studyprivate TO feeding_app;
            public       feeding_app    false    227            �            1259    16814    feed_studyprivate_id_seq    SEQUENCE     z   CREATE SEQUENCE feed_studyprivate_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
 /   DROP SEQUENCE public.feed_studyprivate_id_seq;
       public       feeding_app    false    227    6            ]
           0    0    feed_studyprivate_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE feed_studyprivate_id_seq OWNED BY feed_studyprivate.id;
            public       feeding_app    false    228            ^
           0    0    feed_studyprivate_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('feed_studyprivate_id_seq', 78, true);
            public       feeding_app    false    228            _
           0    0    feed_studyprivate_id_seq    ACL     �   REVOKE ALL ON SEQUENCE feed_studyprivate_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE feed_studyprivate_id_seq FROM feeding_app;
GRANT ALL ON SEQUENCE feed_studyprivate_id_seq TO feeding_app;
            public       feeding_app    false    228            �            1259    16816    feed_subject    TABLE     �  CREATE TABLE feed_subject (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    study_id integer NOT NULL,
    taxon_id integer NOT NULL,
    name character varying(255) NOT NULL,
    breed character varying(255),
    sex character varying(2),
    source character varying(255),
    notes text
);
     DROP TABLE public.feed_subject;
       public         feeding_app    false    6            `
           0    0    feed_subject    ACL     �   REVOKE ALL ON TABLE feed_subject FROM PUBLIC;
REVOKE ALL ON TABLE feed_subject FROM feeding_app;
GRANT ALL ON TABLE feed_subject TO feeding_app;
            public       feeding_app    false    229            �            1259    16822    feed_subject_id_seq    SEQUENCE     u   CREATE SEQUENCE feed_subject_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
 *   DROP SEQUENCE public.feed_subject_id_seq;
       public       feeding_app    false    229    6            a
           0    0    feed_subject_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE feed_subject_id_seq OWNED BY feed_subject.id;
            public       feeding_app    false    230            b
           0    0    feed_subject_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('feed_subject_id_seq', 129, true);
            public       feeding_app    false    230            c
           0    0    feed_subject_id_seq    ACL     �   REVOKE ALL ON SEQUENCE feed_subject_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE feed_subject_id_seq FROM feeding_app;
GRANT ALL ON SEQUENCE feed_subject_id_seq TO feeding_app;
            public       feeding_app    false    230            �            1259    16824 
   feed_taxon    TABLE     _  CREATE TABLE feed_taxon (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    label character varying(255) NOT NULL,
    genus character varying(255) NOT NULL,
    species character varying(255) NOT NULL,
    common_name character varying(255)
);
    DROP TABLE public.feed_taxon;
       public         feeding_app    false    6            d
           0    0 
   feed_taxon    ACL     �   REVOKE ALL ON TABLE feed_taxon FROM PUBLIC;
REVOKE ALL ON TABLE feed_taxon FROM feeding_app;
GRANT ALL ON TABLE feed_taxon TO feeding_app;
            public       feeding_app    false    231            �            1259    16830    feed_taxon_id_seq    SEQUENCE     s   CREATE SEQUENCE feed_taxon_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
 (   DROP SEQUENCE public.feed_taxon_id_seq;
       public       feeding_app    false    231    6            e
           0    0    feed_taxon_id_seq    SEQUENCE OWNED BY     9   ALTER SEQUENCE feed_taxon_id_seq OWNED BY feed_taxon.id;
            public       feeding_app    false    232            f
           0    0    feed_taxon_id_seq    SEQUENCE SET     9   SELECT pg_catalog.setval('feed_taxon_id_seq', 27, true);
            public       feeding_app    false    232            g
           0    0    feed_taxon_id_seq    ACL     �   REVOKE ALL ON SEQUENCE feed_taxon_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE feed_taxon_id_seq FROM feeding_app;
GRANT ALL ON SEQUENCE feed_taxon_id_seq TO feeding_app;
            public       feeding_app    false    232            �            1259    16832 
   feed_trial    TABLE     �  CREATE TABLE feed_trial (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    session_id integer NOT NULL,
    accession character varying(255),
    "position" integer NOT NULL,
    start timestamp with time zone,
    "end" timestamp with time zone,
    bookkeeping character varying(255),
    subj_treatment text,
    subj_notes text,
    food_type character varying(255),
    food_size character varying(255),
    food_property character varying(255),
    behavior_primary_id integer NOT NULL,
    behavior_secondary character varying(255),
    behavior_notes text,
    waveform_picture character varying(100),
    title character varying(255) DEFAULT 'new Trial - edit this'::character varying NOT NULL,
    data_file character varying(100),
    estimated_duration integer,
    CONSTRAINT feed_trial_estimated_duration_check CHECK ((estimated_duration >= 0))
);
    DROP TABLE public.feed_trial;
       public         feeding_app    false    2141    2143    6            h
           0    0 
   feed_trial    ACL     �   REVOKE ALL ON TABLE feed_trial FROM PUBLIC;
REVOKE ALL ON TABLE feed_trial FROM feeding_app;
GRANT ALL ON TABLE feed_trial TO feeding_app;
            public       feeding_app    false    233            �            1259    16840    feed_trial_id_seq    SEQUENCE     s   CREATE SEQUENCE feed_trial_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
 (   DROP SEQUENCE public.feed_trial_id_seq;
       public       feeding_app    false    6    233            i
           0    0    feed_trial_id_seq    SEQUENCE OWNED BY     9   ALTER SEQUENCE feed_trial_id_seq OWNED BY feed_trial.id;
            public       feeding_app    false    234            j
           0    0    feed_trial_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('feed_trial_id_seq', 320, true);
            public       feeding_app    false    234            k
           0    0    feed_trial_id_seq    ACL     �   REVOKE ALL ON SEQUENCE feed_trial_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE feed_trial_id_seq FROM feeding_app;
GRANT ALL ON SEQUENCE feed_trial_id_seq TO feeding_app;
            public       feeding_app    false    234            �            1259    16842 	   feed_unit    TABLE     �   CREATE TABLE feed_unit (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    label character varying(255) NOT NULL,
    technique integer NOT NULL
);
    DROP TABLE public.feed_unit;
       public         feeding_app    false    6            �            1259    16845    feed_unit_id_seq    SEQUENCE     r   CREATE SEQUENCE feed_unit_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
 '   DROP SEQUENCE public.feed_unit_id_seq;
       public       feeding_app    false    6    235            l
           0    0    feed_unit_id_seq    SEQUENCE OWNED BY     7   ALTER SEQUENCE feed_unit_id_seq OWNED BY feed_unit.id;
            public       feeding_app    false    236            m
           0    0    feed_unit_id_seq    SEQUENCE SET     8   SELECT pg_catalog.setval('feed_unit_id_seq', 22, true);
            public       feeding_app    false    236            �            1259    16847    south_migrationhistory    TABLE     �   CREATE TABLE south_migrationhistory (
    id integer NOT NULL,
    app_name character varying(255) NOT NULL,
    migration character varying(255) NOT NULL,
    applied timestamp with time zone
);
 *   DROP TABLE public.south_migrationhistory;
       public         feeding_app    false    6            �            1259    16853    south_migrationhistory_id_seq    SEQUENCE        CREATE SEQUENCE south_migrationhistory_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
 4   DROP SEQUENCE public.south_migrationhistory_id_seq;
       public       feeding_app    false    237    6            n
           0    0    south_migrationhistory_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE south_migrationhistory_id_seq OWNED BY south_migrationhistory.id;
            public       feeding_app    false    238            o
           0    0    south_migrationhistory_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('south_migrationhistory_id_seq', 59, true);
            public       feeding_app    false    238            6           2604    16855    id    DEFAULT     `   ALTER TABLE ONLY auth_group ALTER COLUMN id SET DEFAULT nextval('auth_group_id_seq'::regclass);
 <   ALTER TABLE public.auth_group ALTER COLUMN id DROP DEFAULT;
       public       feeding_app    false    141    140            7           2604    16856    id    DEFAULT     x   ALTER TABLE ONLY auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('auth_group_permissions_id_seq'::regclass);
 H   ALTER TABLE public.auth_group_permissions ALTER COLUMN id DROP DEFAULT;
       public       feeding_app    false    143    142            8           2604    16857    id    DEFAULT     d   ALTER TABLE ONLY auth_message ALTER COLUMN id SET DEFAULT nextval('auth_message_id_seq'::regclass);
 >   ALTER TABLE public.auth_message ALTER COLUMN id DROP DEFAULT;
       public       feeding_app    false    145    144            9           2604    16858    id    DEFAULT     j   ALTER TABLE ONLY auth_permission ALTER COLUMN id SET DEFAULT nextval('auth_permission_id_seq'::regclass);
 A   ALTER TABLE public.auth_permission ALTER COLUMN id DROP DEFAULT;
       public       feeding_app    false    147    146            :           2604    16859    id    DEFAULT     ^   ALTER TABLE ONLY auth_user ALTER COLUMN id SET DEFAULT nextval('auth_user_id_seq'::regclass);
 ;   ALTER TABLE public.auth_user ALTER COLUMN id DROP DEFAULT;
       public       feeding_app    false    151    148            ;           2604    16860    id    DEFAULT     l   ALTER TABLE ONLY auth_user_groups ALTER COLUMN id SET DEFAULT nextval('auth_user_groups_id_seq'::regclass);
 B   ALTER TABLE public.auth_user_groups ALTER COLUMN id DROP DEFAULT;
       public       feeding_app    false    150    149            <           2604    16861    id    DEFAULT     �   ALTER TABLE ONLY auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('auth_user_user_permissions_id_seq'::regclass);
 L   ALTER TABLE public.auth_user_user_permissions ALTER COLUMN id DROP DEFAULT;
       public       feeding_app    false    153    152            =           2604    16862    id    DEFAULT     l   ALTER TABLE ONLY django_admin_log ALTER COLUMN id SET DEFAULT nextval('django_admin_log_id_seq'::regclass);
 B   ALTER TABLE public.django_admin_log ALTER COLUMN id DROP DEFAULT;
       public       feeding_app    false    155    154            ?           2604    16863    id    DEFAULT     r   ALTER TABLE ONLY django_content_type ALTER COLUMN id SET DEFAULT nextval('django_content_type_id_seq'::regclass);
 E   ALTER TABLE public.django_content_type ALTER COLUMN id DROP DEFAULT;
       public       feeding_app    false    157    156            @           2604    16864    id    DEFAULT     b   ALTER TABLE ONLY django_site ALTER COLUMN id SET DEFAULT nextval('django_site_id_seq'::regclass);
 =   ALTER TABLE public.django_site ALTER COLUMN id DROP DEFAULT;
       public       feeding_app    false    160    159            A           2604    16865    id    DEFAULT     j   ALTER TABLE ONLY explorer_bucket ALTER COLUMN id SET DEFAULT nextval('explorer_bucket_id_seq'::regclass);
 A   ALTER TABLE public.explorer_bucket ALTER COLUMN id DROP DEFAULT;
       public       feeding_app    false    162    161            B           2604    16866    id    DEFAULT     x   ALTER TABLE ONLY explorer_trialinbucket ALTER COLUMN id SET DEFAULT nextval('explorer_trialinbucket_id_seq'::regclass);
 H   ALTER TABLE public.explorer_trialinbucket ALTER COLUMN id DROP DEFAULT;
       public       feeding_app    false    164    163            C           2604    16867    id    DEFAULT     d   ALTER TABLE ONLY feed_ageunit ALTER COLUMN id SET DEFAULT nextval('feed_ageunit_id_seq'::regclass);
 >   ALTER TABLE public.feed_ageunit ALTER COLUMN id DROP DEFAULT;
       public       feeding_app    false    166    165            D           2604    16868    id    DEFAULT     z   ALTER TABLE ONLY feed_anatomicallocation ALTER COLUMN id SET DEFAULT nextval('feed_anatomicallocation_id_seq'::regclass);
 I   ALTER TABLE public.feed_anatomicallocation ALTER COLUMN id DROP DEFAULT;
       public       feeding_app    false    168    167            E           2604    16869    id    DEFAULT     �   ALTER TABLE ONLY feed_anteriorposterioraxis ALTER COLUMN id SET DEFAULT nextval('feed_anteriorposterioraxis_id_seq'::regclass);
 L   ALTER TABLE public.feed_anteriorposterioraxis ALTER COLUMN id DROP DEFAULT;
       public       feeding_app    false    170    169            F           2604    16870    id    DEFAULT     f   ALTER TABLE ONLY feed_behavior ALTER COLUMN id SET DEFAULT nextval('feed_behavior_id_seq'::regclass);
 ?   ALTER TABLE public.feed_behavior ALTER COLUMN id DROP DEFAULT;
       public       feeding_app    false    172    171            G           2604    16871    id    DEFAULT     d   ALTER TABLE ONLY feed_channel ALTER COLUMN id SET DEFAULT nextval('feed_channel_id_seq'::regclass);
 >   ALTER TABLE public.feed_channel ALTER COLUMN id DROP DEFAULT;
       public       feeding_app    false    174    173            H           2604    16872    id    DEFAULT     p   ALTER TABLE ONLY feed_channellineup ALTER COLUMN id SET DEFAULT nextval('feed_channellineup_id_seq'::regclass);
 D   ALTER TABLE public.feed_channellineup ALTER COLUMN id DROP DEFAULT;
       public       feeding_app    false    176    175            I           2604    16873    id    DEFAULT     h   ALTER TABLE ONLY feed_depthaxis ALTER COLUMN id SET DEFAULT nextval('feed_depthaxis_id_seq'::regclass);
 @   ALTER TABLE public.feed_depthaxis ALTER COLUMN id DROP DEFAULT;
       public       feeding_app    false    178    177            J           2604    16874    id    DEFAULT     v   ALTER TABLE ONLY feed_developmentstage ALTER COLUMN id SET DEFAULT nextval('feed_developmentstage_id_seq'::regclass);
 G   ALTER TABLE public.feed_developmentstage ALTER COLUMN id DROP DEFAULT;
       public       feeding_app    false    180    179            K           2604    16875    id    DEFAULT     x   ALTER TABLE ONLY feed_dorsalventralaxis ALTER COLUMN id SET DEFAULT nextval('feed_dorsalventralaxis_id_seq'::regclass);
 H   ALTER TABLE public.feed_dorsalventralaxis ALTER COLUMN id DROP DEFAULT;
       public       feeding_app    false    182    181            L           2604    16876    id    DEFAULT     o   ALTER TABLE ONLY feed_electrodetype ALTER COLUMN id SET DEFAULT nextval('feed_eletrodetype_id_seq'::regclass);
 D   ALTER TABLE public.feed_electrodetype ALTER COLUMN id DROP DEFAULT;
       public       feeding_app    false    184    183            M           2604    16877    id    DEFAULT     n   ALTER TABLE ONLY feed_emgfiltering ALTER COLUMN id SET DEFAULT nextval('feed_emgfiltering_id_seq'::regclass);
 C   ALTER TABLE public.feed_emgfiltering ALTER COLUMN id DROP DEFAULT;
       public       feeding_app    false    187    186            O           2604    16878    id    DEFAULT     j   ALTER TABLE ONLY feed_experiment ALTER COLUMN id SET DEFAULT nextval('feed_experiment_id_seq'::regclass);
 A   ALTER TABLE public.feed_experiment ALTER COLUMN id DROP DEFAULT;
       public       feeding_app    false    193    192            P           2604    16879    id    DEFAULT     n   ALTER TABLE ONLY feed_illustration ALTER COLUMN id SET DEFAULT nextval('feed_illustration_id_seq'::regclass);
 C   ALTER TABLE public.feed_illustration ALTER COLUMN id DROP DEFAULT;
       public       feeding_app    false    198    197            Q           2604    16880    id    DEFAULT     x   ALTER TABLE ONLY feed_mediallateralaxis ALTER COLUMN id SET DEFAULT nextval('feed_mediallateralaxis_id_seq'::regclass);
 H   ALTER TABLE public.feed_mediallateralaxis ALTER COLUMN id DROP DEFAULT;
       public       feeding_app    false    203    202            R           2604    16881    id    DEFAULT     z   ALTER TABLE ONLY feed_proximaldistalaxis ALTER COLUMN id SET DEFAULT nextval('feed_proximaldistalaxis_id_seq'::regclass);
 I   ALTER TABLE public.feed_proximaldistalaxis ALTER COLUMN id DROP DEFAULT;
       public       feeding_app    false    208    207            S           2604    16882    id    DEFAULT     h   ALTER TABLE ONLY feed_restraint ALTER COLUMN id SET DEFAULT nextval('feed_restraint_id_seq'::regclass);
 @   ALTER TABLE public.feed_restraint ALTER COLUMN id DROP DEFAULT;
       public       feeding_app    false    210    209            T           2604    16883    id    DEFAULT     b   ALTER TABLE ONLY feed_sensor ALTER COLUMN id SET DEFAULT nextval('feed_sensor_id_seq'::regclass);
 =   ALTER TABLE public.feed_sensor ALTER COLUMN id DROP DEFAULT;
       public       feeding_app    false    212    211            V           2604    16884    id    DEFAULT     d   ALTER TABLE ONLY feed_session ALTER COLUMN id SET DEFAULT nextval('feed_session_id_seq'::regclass);
 >   ALTER TABLE public.feed_session ALTER COLUMN id DROP DEFAULT;
       public       feeding_app    false    214    213            W           2604    16885    id    DEFAULT     `   ALTER TABLE ONLY feed_setup ALTER COLUMN id SET DEFAULT nextval('feed_setup_id_seq'::regclass);
 <   ALTER TABLE public.feed_setup ALTER COLUMN id DROP DEFAULT;
       public       feeding_app    false    216    215            X           2604    16886    id    DEFAULT     ^   ALTER TABLE ONLY feed_side ALTER COLUMN id SET DEFAULT nextval('feed_side_id_seq'::regclass);
 ;   ALTER TABLE public.feed_side ALTER COLUMN id DROP DEFAULT;
       public       feeding_app    false    218    217            Y           2604    16887    id    DEFAULT     `   ALTER TABLE ONLY feed_study ALTER COLUMN id SET DEFAULT nextval('feed_study_id_seq'::regclass);
 <   ALTER TABLE public.feed_study ALTER COLUMN id DROP DEFAULT;
       public       feeding_app    false    226    225            Z           2604    16888    id    DEFAULT     n   ALTER TABLE ONLY feed_studyprivate ALTER COLUMN id SET DEFAULT nextval('feed_studyprivate_id_seq'::regclass);
 C   ALTER TABLE public.feed_studyprivate ALTER COLUMN id DROP DEFAULT;
       public       feeding_app    false    228    227            [           2604    16889    id    DEFAULT     d   ALTER TABLE ONLY feed_subject ALTER COLUMN id SET DEFAULT nextval('feed_subject_id_seq'::regclass);
 >   ALTER TABLE public.feed_subject ALTER COLUMN id DROP DEFAULT;
       public       feeding_app    false    230    229            \           2604    16890    id    DEFAULT     `   ALTER TABLE ONLY feed_taxon ALTER COLUMN id SET DEFAULT nextval('feed_taxon_id_seq'::regclass);
 <   ALTER TABLE public.feed_taxon ALTER COLUMN id DROP DEFAULT;
       public       feeding_app    false    232    231            ^           2604    16891    id    DEFAULT     `   ALTER TABLE ONLY feed_trial ALTER COLUMN id SET DEFAULT nextval('feed_trial_id_seq'::regclass);
 <   ALTER TABLE public.feed_trial ALTER COLUMN id DROP DEFAULT;
       public       feeding_app    false    234    233            `           2604    16892    id    DEFAULT     ^   ALTER TABLE ONLY feed_unit ALTER COLUMN id SET DEFAULT nextval('feed_unit_id_seq'::regclass);
 ;   ALTER TABLE public.feed_unit ALTER COLUMN id DROP DEFAULT;
       public       feeding_app    false    236    235            a           2604    16893    id    DEFAULT     x   ALTER TABLE ONLY south_migrationhistory ALTER COLUMN id SET DEFAULT nextval('south_migrationhistory_id_seq'::regclass);
 H   ALTER TABLE public.south_migrationhistory ALTER COLUMN id DROP DEFAULT;
       public       feeding_app    false    238    237            �	          0    16544 
   auth_group 
   TABLE DATA               '   COPY auth_group (id, name) FROM stdin;
    public       feeding_app    false    140   �      �	          0    16549    auth_group_permissions 
   TABLE DATA               F   COPY auth_group_permissions (id, group_id, permission_id) FROM stdin;
    public       feeding_app    false    142         �	          0    16554    auth_message 
   TABLE DATA               5   COPY auth_message (id, user_id, message) FROM stdin;
    public       feeding_app    false    144   n      �	          0    16562    auth_permission 
   TABLE DATA               G   COPY auth_permission (id, name, content_type_id, codename) FROM stdin;
    public       feeding_app    false    146   �      �	          0    16567 	   auth_user 
   TABLE DATA               �   COPY auth_user (id, username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined) FROM stdin;
    public       feeding_app    false    148   �
      �	          0    16570    auth_user_groups 
   TABLE DATA               :   COPY auth_user_groups (id, user_id, group_id) FROM stdin;
    public       feeding_app    false    149   �      �	          0    16577    auth_user_user_permissions 
   TABLE DATA               I   COPY auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
    public       feeding_app    false    152   D      �	          0    16582    django_admin_log 
   TABLE DATA               �   COPY django_admin_log (id, action_time, user_id, content_type_id, object_id, object_repr, action_flag, change_message) FROM stdin;
    public       feeding_app    false    154   3      �	          0    16591    django_content_type 
   TABLE DATA               B   COPY django_content_type (id, name, app_label, model) FROM stdin;
    public       feeding_app    false    156         �	          0    16596    django_session 
   TABLE DATA               I   COPY django_session (session_key, session_data, expire_date) FROM stdin;
    public       feeding_app    false    158   �      �	          0    16602    django_site 
   TABLE DATA               0   COPY django_site (id, domain, name) FROM stdin;
    public       feeding_app    false    159    3      �	          0    16607    explorer_bucket 
   TABLE DATA               a   COPY explorer_bucket (id, created_by_id, created_at, updated_at, title, description) FROM stdin;
    public       feeding_app    false    161   M3      �	          0    16615    explorer_trialinbucket 
   TABLE DATA               ?   COPY explorer_trialinbucket (id, trial_id, bin_id) FROM stdin;
    public       feeding_app    false    163   47      �	          0    16620    feed_ageunit 
   TABLE DATA               Q   COPY feed_ageunit (id, created_by_id, created_at, updated_at, label) FROM stdin;
    public       feeding_app    false    165   i8      �	          0    16625    feed_anatomicallocation 
   TABLE DATA               f   COPY feed_anatomicallocation (id, created_by_id, created_at, updated_at, label, category) FROM stdin;
    public       feeding_app    false    167   �8      �	          0    16630    feed_anteriorposterioraxis 
   TABLE DATA               _   COPY feed_anteriorposterioraxis (id, created_by_id, created_at, updated_at, label) FROM stdin;
    public       feeding_app    false    169   �=      �	          0    16635    feed_behavior 
   TABLE DATA               R   COPY feed_behavior (id, created_by_id, created_at, updated_at, label) FROM stdin;
    public       feeding_app    false    171   >      �	          0    16640    feed_channel 
   TABLE DATA               g   COPY feed_channel (id, created_by_id, created_at, updated_at, setup_id, name, rate, notes) FROM stdin;
    public       feeding_app    false    173   e?      �	          0    16648    feed_channellineup 
   TABLE DATA               t   COPY feed_channellineup (id, created_by_id, created_at, updated_at, session_id, channel_id, "position") FROM stdin;
    public       feeding_app    false    175   �]      �	          0    16653    feed_depthaxis 
   TABLE DATA               S   COPY feed_depthaxis (id, created_by_id, created_at, updated_at, label) FROM stdin;
    public       feeding_app    false    177   ?v      �	          0    16658    feed_developmentstage 
   TABLE DATA               Z   COPY feed_developmentstage (id, created_by_id, created_at, updated_at, label) FROM stdin;
    public       feeding_app    false    179   �v      �	          0    16663    feed_dorsalventralaxis 
   TABLE DATA               [   COPY feed_dorsalventralaxis (id, created_by_id, created_at, updated_at, label) FROM stdin;
    public       feeding_app    false    181   <w      �	          0    16668    feed_electrodetype 
   TABLE DATA               W   COPY feed_electrodetype (id, created_by_id, created_at, updated_at, label) FROM stdin;
    public       feeding_app    false    183   �w      �	          0    16673    feed_emgchannel 
   TABLE DATA               k   COPY feed_emgchannel (channel_ptr_id, sensor_id, emg_filtering_id, emg_amplification, unit_id) FROM stdin;
    public       feeding_app    false    185   Gx      �	          0    16676    feed_emgfiltering 
   TABLE DATA               V   COPY feed_emgfiltering (id, created_by_id, created_at, updated_at, label) FROM stdin;
    public       feeding_app    false    186   ,      �	          0    16681    feed_emgsensor 
   TABLE DATA               i   COPY feed_emgsensor (sensor_ptr_id, axisdepth_id, electrode_type_id, location_controlled_id) FROM stdin;
    public       feeding_app    false    188   �      �	          0    16684    feed_emgsetup 
   TABLE DATA               <   COPY feed_emgsetup (setup_ptr_id, preamplifier) FROM stdin;
    public       feeding_app    false    189   ��      �	          0    16687    feed_eventchannel 
   TABLE DATA               :   COPY feed_eventchannel (channel_ptr_id, unit) FROM stdin;
    public       feeding_app    false    190   h�      �	          0    16690    feed_eventsetup 
   TABLE DATA               0   COPY feed_eventsetup (setup_ptr_id) FROM stdin;
    public       feeding_app    false    191   ��      �	          0    16693    feed_experiment 
   TABLE DATA               �   COPY feed_experiment (id, created_by_id, created_at, updated_at, study_id, subject_id, accession, start, "end", bookkeeping, description, subj_devstage_id, subj_age, subj_weight, subj_tooth, subject_notes, impl_notes, title, subj_ageunit_id) FROM stdin;
    public       feeding_app    false    192   ��      �	          0    16702    feed_forcechannel 
   TABLE DATA               H   COPY feed_forcechannel (channel_ptr_id, unit_id, sensor_id) FROM stdin;
    public       feeding_app    false    194   ��      �	          0    16705    feed_forcesensor 
   TABLE DATA               2   COPY feed_forcesensor (sensor_ptr_id) FROM stdin;
    public       feeding_app    false    195   �      �	          0    16708    feed_forcesetup 
   TABLE DATA               0   COPY feed_forcesetup (setup_ptr_id) FROM stdin;
    public       feeding_app    false    196   �      �	          0    16711    feed_illustration 
   TABLE DATA               �   COPY feed_illustration (id, created_by_id, created_at, updated_at, picture, notes, subject_id, setup_id, experiment_id) FROM stdin;
    public       feeding_app    false    197   E�      �	          0    16719    feed_kinematicschannel 
   TABLE DATA               M   COPY feed_kinematicschannel (channel_ptr_id, unit_id, sensor_id) FROM stdin;
    public       feeding_app    false    199   ��      �	          0    16722    feed_kinematicssensor 
   TABLE DATA               7   COPY feed_kinematicssensor (sensor_ptr_id) FROM stdin;
    public       feeding_app    false    200    �      �	          0    16725    feed_kinematicssetup 
   TABLE DATA               5   COPY feed_kinematicssetup (setup_ptr_id) FROM stdin;
    public       feeding_app    false    201   n�      �	          0    16728    feed_mediallateralaxis 
   TABLE DATA               [   COPY feed_mediallateralaxis (id, created_by_id, created_at, updated_at, label) FROM stdin;
    public       feeding_app    false    202   ��      �	          0    16733    feed_pressurechannel 
   TABLE DATA               K   COPY feed_pressurechannel (channel_ptr_id, unit_id, sensor_id) FROM stdin;
    public       feeding_app    false    204   ��      �	          0    16736    feed_pressuresensor 
   TABLE DATA               5   COPY feed_pressuresensor (sensor_ptr_id) FROM stdin;
    public       feeding_app    false    205   D�      �	          0    16739    feed_pressuresetup 
   TABLE DATA               3   COPY feed_pressuresetup (setup_ptr_id) FROM stdin;
    public       feeding_app    false    206   |�      �	          0    16742    feed_proximaldistalaxis 
   TABLE DATA               \   COPY feed_proximaldistalaxis (id, created_by_id, created_at, updated_at, label) FROM stdin;
    public       feeding_app    false    207   ��      �	          0    16747    feed_restraint 
   TABLE DATA               S   COPY feed_restraint (id, created_by_id, created_at, updated_at, label) FROM stdin;
    public       feeding_app    false    209   1�      �	          0    16752    feed_sensor 
   TABLE DATA               �   COPY feed_sensor (id, created_by_id, created_at, updated_at, setup_id, name, notes, loc_side_id, location_freetext, loc_ap_id, loc_ml_id, loc_pd_id, loc_dv_id) FROM stdin;
    public       feeding_app    false    211   �      �	          0    16760    feed_session 
   TABLE DATA               �   COPY feed_session (id, created_by_id, created_at, updated_at, experiment_id, accession, start, "end", "position", bookkeeping, subj_restraint_id, subj_anesthesia_sedation, subj_notes, title) FROM stdin;
    public       feeding_app    false    213   ��      �	          0    16769 
   feed_setup 
   TABLE DATA               x   COPY feed_setup (id, created_by_id, created_at, updated_at, experiment_id, notes, sampling_rate, technique) FROM stdin;
    public       feeding_app    false    215   ��      �	          0    16777 	   feed_side 
   TABLE DATA               N   COPY feed_side (id, created_by_id, created_at, updated_at, label) FROM stdin;
    public       feeding_app    false    217   �      �	          0    16782    feed_sonochannel 
   TABLE DATA               V   COPY feed_sonochannel (channel_ptr_id, crystal1_id, crystal2_id, unit_id) FROM stdin;
    public       feeding_app    false    219   ��      �	          0    16785    feed_sonosensor 
   TABLE DATA               W   COPY feed_sonosensor (sensor_ptr_id, axisdepth_id, location_controlled_id) FROM stdin;
    public       feeding_app    false    220   �      �	          0    16788    feed_sonosetup 
   TABLE DATA               ?   COPY feed_sonosetup (setup_ptr_id, sonomicrometer) FROM stdin;
    public       feeding_app    false    221   T�      �	          0    16791    feed_strainchannel 
   TABLE DATA               I   COPY feed_strainchannel (channel_ptr_id, unit_id, sensor_id) FROM stdin;
    public       feeding_app    false    222   ��      �	          0    16794    feed_strainsensor 
   TABLE DATA               3   COPY feed_strainsensor (sensor_ptr_id) FROM stdin;
    public       feeding_app    false    223   
�      �	          0    16797    feed_strainsetup 
   TABLE DATA               1   COPY feed_strainsetup (setup_ptr_id) FROM stdin;
    public       feeding_app    false    224   N�      �	          0    16800 
   feed_study 
   TABLE DATA               �   COPY feed_study (id, created_by_id, created_at, updated_at, accession, bookkeeping, start, "end", funding_agency, approval_secured, description, title, resources) FROM stdin;
    public       feeding_app    false    225   ��      �	          0    16808    feed_studyprivate 
   TABLE DATA               �   COPY feed_studyprivate (id, created_by_id, created_at, updated_at, study_id, pi, organization, lab, funding, approval, notes) FROM stdin;
    public       feeding_app    false    227   b�      �	          0    16816    feed_subject 
   TABLE DATA                  COPY feed_subject (id, created_by_id, created_at, updated_at, study_id, taxon_id, name, breed, sex, source, notes) FROM stdin;
    public       feeding_app    false    229   ��      �	          0    16824 
   feed_taxon 
   TABLE DATA               l   COPY feed_taxon (id, created_by_id, created_at, updated_at, label, genus, species, common_name) FROM stdin;
    public       feeding_app    false    231   l�      �	          0    16832 
   feed_trial 
   TABLE DATA               8  COPY feed_trial (id, created_by_id, created_at, updated_at, session_id, accession, "position", start, "end", bookkeeping, subj_treatment, subj_notes, food_type, food_size, food_property, behavior_primary_id, behavior_secondary, behavior_notes, waveform_picture, title, data_file, estimated_duration) FROM stdin;
    public       feeding_app    false    233   q�      �	          0    16842 	   feed_unit 
   TABLE DATA               Y   COPY feed_unit (id, created_by_id, created_at, updated_at, label, technique) FROM stdin;
    public       feeding_app    false    235   #      �	          0    16847    south_migrationhistory 
   TABLE DATA               K   COPY south_migrationhistory (id, app_name, migration, applied) FROM stdin;
    public       feeding_app    false    237   E      c           2606    16895    auth_group_name_key 
   CONSTRAINT     R   ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);
 H   ALTER TABLE ONLY public.auth_group DROP CONSTRAINT auth_group_name_key;
       public         feeding_app    false    140    140            g           2606    16897 #   auth_group_permissions_group_id_key 
   CONSTRAINT     �   ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_key UNIQUE (group_id, permission_id);
 d   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_group_id_key;
       public         feeding_app    false    142    142    142            i           2606    16899    auth_group_permissions_pkey 
   CONSTRAINT     i   ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);
 \   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_pkey;
       public         feeding_app    false    142    142            e           2606    16901    auth_group_pkey 
   CONSTRAINT     Q   ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.auth_group DROP CONSTRAINT auth_group_pkey;
       public         feeding_app    false    140    140            k           2606    16903    auth_message_pkey 
   CONSTRAINT     U   ALTER TABLE ONLY auth_message
    ADD CONSTRAINT auth_message_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.auth_message DROP CONSTRAINT auth_message_pkey;
       public         feeding_app    false    144    144            o           2606    16905 #   auth_permission_content_type_id_key 
   CONSTRAINT     |   ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_key UNIQUE (content_type_id, codename);
 ]   ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_content_type_id_key;
       public         feeding_app    false    146    146    146            q           2606    16907    auth_permission_pkey 
   CONSTRAINT     [   ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_pkey;
       public         feeding_app    false    146    146            w           2606    16909    auth_user_groups_pkey 
   CONSTRAINT     ]   ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_pkey;
       public         feeding_app    false    149    149            y           2606    16911    auth_user_groups_user_id_key 
   CONSTRAINT     n   ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_key UNIQUE (user_id, group_id);
 W   ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_user_id_key;
       public         feeding_app    false    149    149    149            s           2606    16913    auth_user_pkey 
   CONSTRAINT     O   ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.auth_user DROP CONSTRAINT auth_user_pkey;
       public         feeding_app    false    148    148            {           2606    16915    auth_user_user_permissions_pkey 
   CONSTRAINT     q   ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);
 d   ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permissions_pkey;
       public         feeding_app    false    152    152            }           2606    16917 &   auth_user_user_permissions_user_id_key 
   CONSTRAINT     �   ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_key UNIQUE (user_id, permission_id);
 k   ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permissions_user_id_key;
       public         feeding_app    false    152    152    152            u           2606    16919    auth_user_username_key 
   CONSTRAINT     X   ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);
 J   ALTER TABLE ONLY public.auth_user DROP CONSTRAINT auth_user_username_key;
       public         feeding_app    false    148    148            �           2606    16921    django_admin_log_pkey 
   CONSTRAINT     ]   ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_pkey;
       public         feeding_app    false    154    154            �           2606    16923 !   django_content_type_app_label_key 
   CONSTRAINT     u   ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_app_label_key UNIQUE (app_label, model);
 _   ALTER TABLE ONLY public.django_content_type DROP CONSTRAINT django_content_type_app_label_key;
       public         feeding_app    false    156    156    156            �           2606    16925    django_content_type_pkey 
   CONSTRAINT     c   ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);
 V   ALTER TABLE ONLY public.django_content_type DROP CONSTRAINT django_content_type_pkey;
       public         feeding_app    false    156    156            �           2606    16927    django_session_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);
 L   ALTER TABLE ONLY public.django_session DROP CONSTRAINT django_session_pkey;
       public         feeding_app    false    158    158            �           2606    16929    django_site_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY django_site
    ADD CONSTRAINT django_site_pkey PRIMARY KEY (id);
 F   ALTER TABLE ONLY public.django_site DROP CONSTRAINT django_site_pkey;
       public         feeding_app    false    159    159            �           2606    16931    explorer_bucket_pkey 
   CONSTRAINT     [   ALTER TABLE ONLY explorer_bucket
    ADD CONSTRAINT explorer_bucket_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.explorer_bucket DROP CONSTRAINT explorer_bucket_pkey;
       public         feeding_app    false    161    161            �           2606    16933    explorer_trialinbucket_pkey 
   CONSTRAINT     i   ALTER TABLE ONLY explorer_trialinbucket
    ADD CONSTRAINT explorer_trialinbucket_pkey PRIMARY KEY (id);
 \   ALTER TABLE ONLY public.explorer_trialinbucket DROP CONSTRAINT explorer_trialinbucket_pkey;
       public         feeding_app    false    163    163            �           2606    16935    feed_ageunit_pkey 
   CONSTRAINT     U   ALTER TABLE ONLY feed_ageunit
    ADD CONSTRAINT feed_ageunit_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.feed_ageunit DROP CONSTRAINT feed_ageunit_pkey;
       public         feeding_app    false    165    165            �           2606    16937    feed_anatomicallocation_pkey 
   CONSTRAINT     k   ALTER TABLE ONLY feed_anatomicallocation
    ADD CONSTRAINT feed_anatomicallocation_pkey PRIMARY KEY (id);
 ^   ALTER TABLE ONLY public.feed_anatomicallocation DROP CONSTRAINT feed_anatomicallocation_pkey;
       public         feeding_app    false    167    167            �           2606    16939    feed_anteriorposterioraxis_pkey 
   CONSTRAINT     q   ALTER TABLE ONLY feed_anteriorposterioraxis
    ADD CONSTRAINT feed_anteriorposterioraxis_pkey PRIMARY KEY (id);
 d   ALTER TABLE ONLY public.feed_anteriorposterioraxis DROP CONSTRAINT feed_anteriorposterioraxis_pkey;
       public         feeding_app    false    169    169            �           2606    16941    feed_behavior_pkey 
   CONSTRAINT     W   ALTER TABLE ONLY feed_behavior
    ADD CONSTRAINT feed_behavior_pkey PRIMARY KEY (id);
 J   ALTER TABLE ONLY public.feed_behavior DROP CONSTRAINT feed_behavior_pkey;
       public         feeding_app    false    171    171            �           2606    16943    feed_channel_pkey 
   CONSTRAINT     U   ALTER TABLE ONLY feed_channel
    ADD CONSTRAINT feed_channel_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.feed_channel DROP CONSTRAINT feed_channel_pkey;
       public         feeding_app    false    173    173            �           2606    16945    feed_channellineup_pkey 
   CONSTRAINT     a   ALTER TABLE ONLY feed_channellineup
    ADD CONSTRAINT feed_channellineup_pkey PRIMARY KEY (id);
 T   ALTER TABLE ONLY public.feed_channellineup DROP CONSTRAINT feed_channellineup_pkey;
       public         feeding_app    false    175    175            �           2606    16947    feed_depthaxis_pkey 
   CONSTRAINT     Y   ALTER TABLE ONLY feed_depthaxis
    ADD CONSTRAINT feed_depthaxis_pkey PRIMARY KEY (id);
 L   ALTER TABLE ONLY public.feed_depthaxis DROP CONSTRAINT feed_depthaxis_pkey;
       public         feeding_app    false    177    177            �           2606    16949    feed_developmentstage_pkey 
   CONSTRAINT     g   ALTER TABLE ONLY feed_developmentstage
    ADD CONSTRAINT feed_developmentstage_pkey PRIMARY KEY (id);
 Z   ALTER TABLE ONLY public.feed_developmentstage DROP CONSTRAINT feed_developmentstage_pkey;
       public         feeding_app    false    179    179            �           2606    16951    feed_dorsalventralaxis_pkey 
   CONSTRAINT     i   ALTER TABLE ONLY feed_dorsalventralaxis
    ADD CONSTRAINT feed_dorsalventralaxis_pkey PRIMARY KEY (id);
 \   ALTER TABLE ONLY public.feed_dorsalventralaxis DROP CONSTRAINT feed_dorsalventralaxis_pkey;
       public         feeding_app    false    181    181            �           2606    16953    feed_eletrodetype_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY feed_electrodetype
    ADD CONSTRAINT feed_eletrodetype_pkey PRIMARY KEY (id);
 S   ALTER TABLE ONLY public.feed_electrodetype DROP CONSTRAINT feed_eletrodetype_pkey;
       public         feeding_app    false    183    183            �           2606    16955    feed_emgchannel_pkey 
   CONSTRAINT     g   ALTER TABLE ONLY feed_emgchannel
    ADD CONSTRAINT feed_emgchannel_pkey PRIMARY KEY (channel_ptr_id);
 N   ALTER TABLE ONLY public.feed_emgchannel DROP CONSTRAINT feed_emgchannel_pkey;
       public         feeding_app    false    185    185            �           2606    16957    feed_emgfiltering_pkey 
   CONSTRAINT     _   ALTER TABLE ONLY feed_emgfiltering
    ADD CONSTRAINT feed_emgfiltering_pkey PRIMARY KEY (id);
 R   ALTER TABLE ONLY public.feed_emgfiltering DROP CONSTRAINT feed_emgfiltering_pkey;
       public         feeding_app    false    186    186            �           2606    16959    feed_emgsensor_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY feed_emgsensor
    ADD CONSTRAINT feed_emgsensor_pkey PRIMARY KEY (sensor_ptr_id);
 L   ALTER TABLE ONLY public.feed_emgsensor DROP CONSTRAINT feed_emgsensor_pkey;
       public         feeding_app    false    188    188            �           2606    16961    feed_emgsetup_pkey 
   CONSTRAINT     a   ALTER TABLE ONLY feed_emgsetup
    ADD CONSTRAINT feed_emgsetup_pkey PRIMARY KEY (setup_ptr_id);
 J   ALTER TABLE ONLY public.feed_emgsetup DROP CONSTRAINT feed_emgsetup_pkey;
       public         feeding_app    false    189    189            �           2606    16963    feed_eventchannel_pkey 
   CONSTRAINT     k   ALTER TABLE ONLY feed_eventchannel
    ADD CONSTRAINT feed_eventchannel_pkey PRIMARY KEY (channel_ptr_id);
 R   ALTER TABLE ONLY public.feed_eventchannel DROP CONSTRAINT feed_eventchannel_pkey;
       public         feeding_app    false    190    190            �           2606    16965    feed_eventsetup_pkey 
   CONSTRAINT     e   ALTER TABLE ONLY feed_eventsetup
    ADD CONSTRAINT feed_eventsetup_pkey PRIMARY KEY (setup_ptr_id);
 N   ALTER TABLE ONLY public.feed_eventsetup DROP CONSTRAINT feed_eventsetup_pkey;
       public         feeding_app    false    191    191            �           2606    16967    feed_experiment_pkey 
   CONSTRAINT     [   ALTER TABLE ONLY feed_experiment
    ADD CONSTRAINT feed_experiment_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.feed_experiment DROP CONSTRAINT feed_experiment_pkey;
       public         feeding_app    false    192    192            �           2606    16969    feed_forcechannel_pkey 
   CONSTRAINT     k   ALTER TABLE ONLY feed_forcechannel
    ADD CONSTRAINT feed_forcechannel_pkey PRIMARY KEY (channel_ptr_id);
 R   ALTER TABLE ONLY public.feed_forcechannel DROP CONSTRAINT feed_forcechannel_pkey;
       public         feeding_app    false    194    194            �           2606    16971    feed_forcesensor_pkey 
   CONSTRAINT     h   ALTER TABLE ONLY feed_forcesensor
    ADD CONSTRAINT feed_forcesensor_pkey PRIMARY KEY (sensor_ptr_id);
 P   ALTER TABLE ONLY public.feed_forcesensor DROP CONSTRAINT feed_forcesensor_pkey;
       public         feeding_app    false    195    195            �           2606    16973    feed_forcesetup_pkey 
   CONSTRAINT     e   ALTER TABLE ONLY feed_forcesetup
    ADD CONSTRAINT feed_forcesetup_pkey PRIMARY KEY (setup_ptr_id);
 N   ALTER TABLE ONLY public.feed_forcesetup DROP CONSTRAINT feed_forcesetup_pkey;
       public         feeding_app    false    196    196            �           2606    16975    feed_illustration_pkey 
   CONSTRAINT     _   ALTER TABLE ONLY feed_illustration
    ADD CONSTRAINT feed_illustration_pkey PRIMARY KEY (id);
 R   ALTER TABLE ONLY public.feed_illustration DROP CONSTRAINT feed_illustration_pkey;
       public         feeding_app    false    197    197            �           2606    16977    feed_kinematicschannel_pkey 
   CONSTRAINT     u   ALTER TABLE ONLY feed_kinematicschannel
    ADD CONSTRAINT feed_kinematicschannel_pkey PRIMARY KEY (channel_ptr_id);
 \   ALTER TABLE ONLY public.feed_kinematicschannel DROP CONSTRAINT feed_kinematicschannel_pkey;
       public         feeding_app    false    199    199            �           2606    16979    feed_kinematicssensor_pkey 
   CONSTRAINT     r   ALTER TABLE ONLY feed_kinematicssensor
    ADD CONSTRAINT feed_kinematicssensor_pkey PRIMARY KEY (sensor_ptr_id);
 Z   ALTER TABLE ONLY public.feed_kinematicssensor DROP CONSTRAINT feed_kinematicssensor_pkey;
       public         feeding_app    false    200    200            �           2606    16981    feed_kinematicssetup_pkey 
   CONSTRAINT     o   ALTER TABLE ONLY feed_kinematicssetup
    ADD CONSTRAINT feed_kinematicssetup_pkey PRIMARY KEY (setup_ptr_id);
 X   ALTER TABLE ONLY public.feed_kinematicssetup DROP CONSTRAINT feed_kinematicssetup_pkey;
       public         feeding_app    false    201    201            �           2606    16983    feed_mediallateralaxis_pkey 
   CONSTRAINT     i   ALTER TABLE ONLY feed_mediallateralaxis
    ADD CONSTRAINT feed_mediallateralaxis_pkey PRIMARY KEY (id);
 \   ALTER TABLE ONLY public.feed_mediallateralaxis DROP CONSTRAINT feed_mediallateralaxis_pkey;
       public         feeding_app    false    202    202            �           2606    16985    feed_pressurechannel_pkey 
   CONSTRAINT     q   ALTER TABLE ONLY feed_pressurechannel
    ADD CONSTRAINT feed_pressurechannel_pkey PRIMARY KEY (channel_ptr_id);
 X   ALTER TABLE ONLY public.feed_pressurechannel DROP CONSTRAINT feed_pressurechannel_pkey;
       public         feeding_app    false    204    204            �           2606    16987    feed_pressuresensor_pkey 
   CONSTRAINT     n   ALTER TABLE ONLY feed_pressuresensor
    ADD CONSTRAINT feed_pressuresensor_pkey PRIMARY KEY (sensor_ptr_id);
 V   ALTER TABLE ONLY public.feed_pressuresensor DROP CONSTRAINT feed_pressuresensor_pkey;
       public         feeding_app    false    205    205            �           2606    16989    feed_pressuresetup_pkey 
   CONSTRAINT     k   ALTER TABLE ONLY feed_pressuresetup
    ADD CONSTRAINT feed_pressuresetup_pkey PRIMARY KEY (setup_ptr_id);
 T   ALTER TABLE ONLY public.feed_pressuresetup DROP CONSTRAINT feed_pressuresetup_pkey;
       public         feeding_app    false    206    206            �           2606    16991    feed_proximaldistalaxis_pkey 
   CONSTRAINT     k   ALTER TABLE ONLY feed_proximaldistalaxis
    ADD CONSTRAINT feed_proximaldistalaxis_pkey PRIMARY KEY (id);
 ^   ALTER TABLE ONLY public.feed_proximaldistalaxis DROP CONSTRAINT feed_proximaldistalaxis_pkey;
       public         feeding_app    false    207    207            �           2606    16993    feed_restraint_pkey 
   CONSTRAINT     Y   ALTER TABLE ONLY feed_restraint
    ADD CONSTRAINT feed_restraint_pkey PRIMARY KEY (id);
 L   ALTER TABLE ONLY public.feed_restraint DROP CONSTRAINT feed_restraint_pkey;
       public         feeding_app    false    209    209            �           2606    16995    feed_sensor_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY feed_sensor
    ADD CONSTRAINT feed_sensor_pkey PRIMARY KEY (id);
 F   ALTER TABLE ONLY public.feed_sensor DROP CONSTRAINT feed_sensor_pkey;
       public         feeding_app    false    211    211            �           2606    16997    feed_session_pkey 
   CONSTRAINT     U   ALTER TABLE ONLY feed_session
    ADD CONSTRAINT feed_session_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.feed_session DROP CONSTRAINT feed_session_pkey;
       public         feeding_app    false    213    213            	           2606    16999    feed_setup_pkey 
   CONSTRAINT     Q   ALTER TABLE ONLY feed_setup
    ADD CONSTRAINT feed_setup_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.feed_setup DROP CONSTRAINT feed_setup_pkey;
       public         feeding_app    false    215    215            	           2606    17001    feed_side_pkey 
   CONSTRAINT     O   ALTER TABLE ONLY feed_side
    ADD CONSTRAINT feed_side_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.feed_side DROP CONSTRAINT feed_side_pkey;
       public         feeding_app    false    217    217            	           2606    17003    feed_sonochannel_pkey 
   CONSTRAINT     i   ALTER TABLE ONLY feed_sonochannel
    ADD CONSTRAINT feed_sonochannel_pkey PRIMARY KEY (channel_ptr_id);
 P   ALTER TABLE ONLY public.feed_sonochannel DROP CONSTRAINT feed_sonochannel_pkey;
       public         feeding_app    false    219    219            	           2606    17005    feed_sonosensor_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY feed_sonosensor
    ADD CONSTRAINT feed_sonosensor_pkey PRIMARY KEY (sensor_ptr_id);
 N   ALTER TABLE ONLY public.feed_sonosensor DROP CONSTRAINT feed_sonosensor_pkey;
       public         feeding_app    false    220    220            	           2606    17007    feed_sonosetup_pkey 
   CONSTRAINT     c   ALTER TABLE ONLY feed_sonosetup
    ADD CONSTRAINT feed_sonosetup_pkey PRIMARY KEY (setup_ptr_id);
 L   ALTER TABLE ONLY public.feed_sonosetup DROP CONSTRAINT feed_sonosetup_pkey;
       public         feeding_app    false    221    221            	           2606    17009    feed_strainchannel_pkey 
   CONSTRAINT     m   ALTER TABLE ONLY feed_strainchannel
    ADD CONSTRAINT feed_strainchannel_pkey PRIMARY KEY (channel_ptr_id);
 T   ALTER TABLE ONLY public.feed_strainchannel DROP CONSTRAINT feed_strainchannel_pkey;
       public         feeding_app    false    222    222            	           2606    17011    feed_strainsensor_pkey 
   CONSTRAINT     j   ALTER TABLE ONLY feed_strainsensor
    ADD CONSTRAINT feed_strainsensor_pkey PRIMARY KEY (sensor_ptr_id);
 R   ALTER TABLE ONLY public.feed_strainsensor DROP CONSTRAINT feed_strainsensor_pkey;
       public         feeding_app    false    223    223            	           2606    17013    feed_strainsetup_pkey 
   CONSTRAINT     g   ALTER TABLE ONLY feed_strainsetup
    ADD CONSTRAINT feed_strainsetup_pkey PRIMARY KEY (setup_ptr_id);
 P   ALTER TABLE ONLY public.feed_strainsetup DROP CONSTRAINT feed_strainsetup_pkey;
       public         feeding_app    false    224    224            	           2606    17015    feed_study_pkey 
   CONSTRAINT     Q   ALTER TABLE ONLY feed_study
    ADD CONSTRAINT feed_study_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.feed_study DROP CONSTRAINT feed_study_pkey;
       public         feeding_app    false    225    225             	           2606    17017    feed_studyprivate_pkey 
   CONSTRAINT     _   ALTER TABLE ONLY feed_studyprivate
    ADD CONSTRAINT feed_studyprivate_pkey PRIMARY KEY (id);
 R   ALTER TABLE ONLY public.feed_studyprivate DROP CONSTRAINT feed_studyprivate_pkey;
       public         feeding_app    false    227    227            $	           2606    17019    feed_subject_pkey 
   CONSTRAINT     U   ALTER TABLE ONLY feed_subject
    ADD CONSTRAINT feed_subject_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.feed_subject DROP CONSTRAINT feed_subject_pkey;
       public         feeding_app    false    229    229            )	           2606    17021    feed_taxon_pkey 
   CONSTRAINT     Q   ALTER TABLE ONLY feed_taxon
    ADD CONSTRAINT feed_taxon_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.feed_taxon DROP CONSTRAINT feed_taxon_pkey;
       public         feeding_app    false    231    231            -	           2606    17023    feed_trial_pkey 
   CONSTRAINT     Q   ALTER TABLE ONLY feed_trial
    ADD CONSTRAINT feed_trial_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.feed_trial DROP CONSTRAINT feed_trial_pkey;
       public         feeding_app    false    233    233            1	           2606    17025    feed_unit_pkey 
   CONSTRAINT     O   ALTER TABLE ONLY feed_unit
    ADD CONSTRAINT feed_unit_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.feed_unit DROP CONSTRAINT feed_unit_pkey;
       public         feeding_app    false    235    235            3	           2606    17027    south_migrationhistory_pkey 
   CONSTRAINT     i   ALTER TABLE ONLY south_migrationhistory
    ADD CONSTRAINT south_migrationhistory_pkey PRIMARY KEY (id);
 \   ALTER TABLE ONLY public.south_migrationhistory DROP CONSTRAINT south_migrationhistory_pkey;
       public         feeding_app    false    237    237            l           1259    17028    auth_message_user_id    INDEX     I   CREATE INDEX auth_message_user_id ON auth_message USING btree (user_id);
 (   DROP INDEX public.auth_message_user_id;
       public         feeding_app    false    144            m           1259    17029    auth_permission_content_type_id    INDEX     _   CREATE INDEX auth_permission_content_type_id ON auth_permission USING btree (content_type_id);
 3   DROP INDEX public.auth_permission_content_type_id;
       public         feeding_app    false    146            ~           1259    17030     django_admin_log_content_type_id    INDEX     a   CREATE INDEX django_admin_log_content_type_id ON django_admin_log USING btree (content_type_id);
 4   DROP INDEX public.django_admin_log_content_type_id;
       public         feeding_app    false    154            �           1259    17031    django_admin_log_user_id    INDEX     Q   CREATE INDEX django_admin_log_user_id ON django_admin_log USING btree (user_id);
 ,   DROP INDEX public.django_admin_log_user_id;
       public         feeding_app    false    154            �           1259    17032    explorer_bucket_created_by_id    INDEX     [   CREATE INDEX explorer_bucket_created_by_id ON explorer_bucket USING btree (created_by_id);
 1   DROP INDEX public.explorer_bucket_created_by_id;
       public         feeding_app    false    161            �           1259    17033    explorer_trialinbucket_bin_id    INDEX     [   CREATE INDEX explorer_trialinbucket_bin_id ON explorer_trialinbucket USING btree (bin_id);
 1   DROP INDEX public.explorer_trialinbucket_bin_id;
       public         feeding_app    false    163            �           1259    17034    explorer_trialinbucket_trial_id    INDEX     _   CREATE INDEX explorer_trialinbucket_trial_id ON explorer_trialinbucket USING btree (trial_id);
 3   DROP INDEX public.explorer_trialinbucket_trial_id;
       public         feeding_app    false    163            �           1259    17035    feed_ageunit_created_by_id    INDEX     U   CREATE INDEX feed_ageunit_created_by_id ON feed_ageunit USING btree (created_by_id);
 .   DROP INDEX public.feed_ageunit_created_by_id;
       public         feeding_app    false    165            �           1259    17036 %   feed_anatomicallocation_created_by_id    INDEX     k   CREATE INDEX feed_anatomicallocation_created_by_id ON feed_anatomicallocation USING btree (created_by_id);
 9   DROP INDEX public.feed_anatomicallocation_created_by_id;
       public         feeding_app    false    167            �           1259    17037 (   feed_anteriorposterioraxis_created_by_id    INDEX     q   CREATE INDEX feed_anteriorposterioraxis_created_by_id ON feed_anteriorposterioraxis USING btree (created_by_id);
 <   DROP INDEX public.feed_anteriorposterioraxis_created_by_id;
       public         feeding_app    false    169            �           1259    17038    feed_behavior_created_by_id    INDEX     W   CREATE INDEX feed_behavior_created_by_id ON feed_behavior USING btree (created_by_id);
 /   DROP INDEX public.feed_behavior_created_by_id;
       public         feeding_app    false    171            �           1259    17039    feed_channel_created_by_id    INDEX     U   CREATE INDEX feed_channel_created_by_id ON feed_channel USING btree (created_by_id);
 .   DROP INDEX public.feed_channel_created_by_id;
       public         feeding_app    false    173            �           1259    17040    feed_channel_setup_id    INDEX     K   CREATE INDEX feed_channel_setup_id ON feed_channel USING btree (setup_id);
 )   DROP INDEX public.feed_channel_setup_id;
       public         feeding_app    false    173            �           1259    17041    feed_channellineup_channel_id    INDEX     [   CREATE INDEX feed_channellineup_channel_id ON feed_channellineup USING btree (channel_id);
 1   DROP INDEX public.feed_channellineup_channel_id;
       public         feeding_app    false    175            �           1259    17042     feed_channellineup_created_by_id    INDEX     a   CREATE INDEX feed_channellineup_created_by_id ON feed_channellineup USING btree (created_by_id);
 4   DROP INDEX public.feed_channellineup_created_by_id;
       public         feeding_app    false    175            �           1259    17043    feed_channellineup_session_id    INDEX     [   CREATE INDEX feed_channellineup_session_id ON feed_channellineup USING btree (session_id);
 1   DROP INDEX public.feed_channellineup_session_id;
       public         feeding_app    false    175            �           1259    17044    feed_depthaxis_created_by_id    INDEX     Y   CREATE INDEX feed_depthaxis_created_by_id ON feed_depthaxis USING btree (created_by_id);
 0   DROP INDEX public.feed_depthaxis_created_by_id;
       public         feeding_app    false    177            �           1259    17045 #   feed_developmentstage_created_by_id    INDEX     g   CREATE INDEX feed_developmentstage_created_by_id ON feed_developmentstage USING btree (created_by_id);
 7   DROP INDEX public.feed_developmentstage_created_by_id;
       public         feeding_app    false    179            �           1259    17046 $   feed_dorsalventralaxis_created_by_id    INDEX     i   CREATE INDEX feed_dorsalventralaxis_created_by_id ON feed_dorsalventralaxis USING btree (created_by_id);
 8   DROP INDEX public.feed_dorsalventralaxis_created_by_id;
       public         feeding_app    false    181            �           1259    17047    feed_eletrodetype_created_by_id    INDEX     `   CREATE INDEX feed_eletrodetype_created_by_id ON feed_electrodetype USING btree (created_by_id);
 3   DROP INDEX public.feed_eletrodetype_created_by_id;
       public         feeding_app    false    183            �           1259    17048     feed_emgchannel_emg_filtering_id    INDEX     a   CREATE INDEX feed_emgchannel_emg_filtering_id ON feed_emgchannel USING btree (emg_filtering_id);
 4   DROP INDEX public.feed_emgchannel_emg_filtering_id;
       public         feeding_app    false    185            �           1259    17049    feed_emgchannel_sensor_id    INDEX     S   CREATE INDEX feed_emgchannel_sensor_id ON feed_emgchannel USING btree (sensor_id);
 -   DROP INDEX public.feed_emgchannel_sensor_id;
       public         feeding_app    false    185            �           1259    17050    feed_emgchannel_unit_id    INDEX     O   CREATE INDEX feed_emgchannel_unit_id ON feed_emgchannel USING btree (unit_id);
 +   DROP INDEX public.feed_emgchannel_unit_id;
       public         feeding_app    false    185            �           1259    17051    feed_emgfiltering_created_by_id    INDEX     _   CREATE INDEX feed_emgfiltering_created_by_id ON feed_emgfiltering USING btree (created_by_id);
 3   DROP INDEX public.feed_emgfiltering_created_by_id;
       public         feeding_app    false    186            �           1259    17052    feed_emgsensor_axisdepth_id    INDEX     W   CREATE INDEX feed_emgsensor_axisdepth_id ON feed_emgsensor USING btree (axisdepth_id);
 /   DROP INDEX public.feed_emgsensor_axisdepth_id;
       public         feeding_app    false    188            �           1259    17053    feed_emgsensor_eletrode_type_id    INDEX     `   CREATE INDEX feed_emgsensor_eletrode_type_id ON feed_emgsensor USING btree (electrode_type_id);
 3   DROP INDEX public.feed_emgsensor_eletrode_type_id;
       public         feeding_app    false    188            �           1259    17054 %   feed_emgsensor_location_controlled_id    INDEX     k   CREATE INDEX feed_emgsensor_location_controlled_id ON feed_emgsensor USING btree (location_controlled_id);
 9   DROP INDEX public.feed_emgsensor_location_controlled_id;
       public         feeding_app    false    188            �           1259    17055    feed_experiment_created_by_id    INDEX     [   CREATE INDEX feed_experiment_created_by_id ON feed_experiment USING btree (created_by_id);
 1   DROP INDEX public.feed_experiment_created_by_id;
       public         feeding_app    false    192            �           1259    17056    feed_experiment_study_id    INDEX     Q   CREATE INDEX feed_experiment_study_id ON feed_experiment USING btree (study_id);
 ,   DROP INDEX public.feed_experiment_study_id;
       public         feeding_app    false    192            �           1259    17057    feed_experiment_subj_ageunit_id    INDEX     _   CREATE INDEX feed_experiment_subj_ageunit_id ON feed_experiment USING btree (subj_ageunit_id);
 3   DROP INDEX public.feed_experiment_subj_ageunit_id;
       public         feeding_app    false    192            �           1259    17058     feed_experiment_subj_devstage_id    INDEX     a   CREATE INDEX feed_experiment_subj_devstage_id ON feed_experiment USING btree (subj_devstage_id);
 4   DROP INDEX public.feed_experiment_subj_devstage_id;
       public         feeding_app    false    192            �           1259    17059    feed_experiment_subject_id    INDEX     U   CREATE INDEX feed_experiment_subject_id ON feed_experiment USING btree (subject_id);
 .   DROP INDEX public.feed_experiment_subject_id;
       public         feeding_app    false    192            �           1259    17060    feed_forcechannel_sensor_id    INDEX     W   CREATE INDEX feed_forcechannel_sensor_id ON feed_forcechannel USING btree (sensor_id);
 /   DROP INDEX public.feed_forcechannel_sensor_id;
       public         feeding_app    false    194            �           1259    17061    feed_forcechannel_unit_id    INDEX     S   CREATE INDEX feed_forcechannel_unit_id ON feed_forcechannel USING btree (unit_id);
 -   DROP INDEX public.feed_forcechannel_unit_id;
       public         feeding_app    false    194            �           1259    17062    feed_illustration_created_by_id    INDEX     _   CREATE INDEX feed_illustration_created_by_id ON feed_illustration USING btree (created_by_id);
 3   DROP INDEX public.feed_illustration_created_by_id;
       public         feeding_app    false    197            �           1259    17063    feed_illustration_experiment_id    INDEX     _   CREATE INDEX feed_illustration_experiment_id ON feed_illustration USING btree (experiment_id);
 3   DROP INDEX public.feed_illustration_experiment_id;
       public         feeding_app    false    197            �           1259    17064    feed_illustration_setup_id    INDEX     U   CREATE INDEX feed_illustration_setup_id ON feed_illustration USING btree (setup_id);
 .   DROP INDEX public.feed_illustration_setup_id;
       public         feeding_app    false    197            �           1259    17065    feed_illustration_subject_id    INDEX     Y   CREATE INDEX feed_illustration_subject_id ON feed_illustration USING btree (subject_id);
 0   DROP INDEX public.feed_illustration_subject_id;
       public         feeding_app    false    197            �           1259    17066     feed_kinematicschannel_sensor_id    INDEX     a   CREATE INDEX feed_kinematicschannel_sensor_id ON feed_kinematicschannel USING btree (sensor_id);
 4   DROP INDEX public.feed_kinematicschannel_sensor_id;
       public         feeding_app    false    199            �           1259    17067    feed_kinematicschannel_unit_id    INDEX     ]   CREATE INDEX feed_kinematicschannel_unit_id ON feed_kinematicschannel USING btree (unit_id);
 2   DROP INDEX public.feed_kinematicschannel_unit_id;
       public         feeding_app    false    199            �           1259    17068 $   feed_mediallateralaxis_created_by_id    INDEX     i   CREATE INDEX feed_mediallateralaxis_created_by_id ON feed_mediallateralaxis USING btree (created_by_id);
 8   DROP INDEX public.feed_mediallateralaxis_created_by_id;
       public         feeding_app    false    202            �           1259    17069    feed_pressurechannel_sensor_id    INDEX     ]   CREATE INDEX feed_pressurechannel_sensor_id ON feed_pressurechannel USING btree (sensor_id);
 2   DROP INDEX public.feed_pressurechannel_sensor_id;
       public         feeding_app    false    204            �           1259    17070    feed_pressurechannel_unit_id    INDEX     Y   CREATE INDEX feed_pressurechannel_unit_id ON feed_pressurechannel USING btree (unit_id);
 0   DROP INDEX public.feed_pressurechannel_unit_id;
       public         feeding_app    false    204            �           1259    17071 %   feed_proximaldistalaxis_created_by_id    INDEX     k   CREATE INDEX feed_proximaldistalaxis_created_by_id ON feed_proximaldistalaxis USING btree (created_by_id);
 9   DROP INDEX public.feed_proximaldistalaxis_created_by_id;
       public         feeding_app    false    207            �           1259    17072    feed_restraint_created_by_id    INDEX     Y   CREATE INDEX feed_restraint_created_by_id ON feed_restraint USING btree (created_by_id);
 0   DROP INDEX public.feed_restraint_created_by_id;
       public         feeding_app    false    209            �           1259    17073    feed_sensor_created_by_id    INDEX     S   CREATE INDEX feed_sensor_created_by_id ON feed_sensor USING btree (created_by_id);
 -   DROP INDEX public.feed_sensor_created_by_id;
       public         feeding_app    false    211            �           1259    17074    feed_sensor_loc_ap_id    INDEX     K   CREATE INDEX feed_sensor_loc_ap_id ON feed_sensor USING btree (loc_ap_id);
 )   DROP INDEX public.feed_sensor_loc_ap_id;
       public         feeding_app    false    211            �           1259    17075    feed_sensor_loc_dv_id    INDEX     K   CREATE INDEX feed_sensor_loc_dv_id ON feed_sensor USING btree (loc_dv_id);
 )   DROP INDEX public.feed_sensor_loc_dv_id;
       public         feeding_app    false    211            �           1259    17076    feed_sensor_loc_ml_id    INDEX     K   CREATE INDEX feed_sensor_loc_ml_id ON feed_sensor USING btree (loc_ml_id);
 )   DROP INDEX public.feed_sensor_loc_ml_id;
       public         feeding_app    false    211            �           1259    17077    feed_sensor_loc_pd_id    INDEX     K   CREATE INDEX feed_sensor_loc_pd_id ON feed_sensor USING btree (loc_pd_id);
 )   DROP INDEX public.feed_sensor_loc_pd_id;
       public         feeding_app    false    211            �           1259    17078    feed_sensor_loc_side_id    INDEX     O   CREATE INDEX feed_sensor_loc_side_id ON feed_sensor USING btree (loc_side_id);
 +   DROP INDEX public.feed_sensor_loc_side_id;
       public         feeding_app    false    211            �           1259    17079    feed_sensor_setup_id    INDEX     I   CREATE INDEX feed_sensor_setup_id ON feed_sensor USING btree (setup_id);
 (   DROP INDEX public.feed_sensor_setup_id;
       public         feeding_app    false    211            �           1259    17080    feed_session_created_by_id    INDEX     U   CREATE INDEX feed_session_created_by_id ON feed_session USING btree (created_by_id);
 .   DROP INDEX public.feed_session_created_by_id;
       public         feeding_app    false    213            �           1259    17081    feed_session_experiment_id    INDEX     U   CREATE INDEX feed_session_experiment_id ON feed_session USING btree (experiment_id);
 .   DROP INDEX public.feed_session_experiment_id;
       public         feeding_app    false    213             	           1259    17082    feed_session_subj_restraint_id    INDEX     ]   CREATE INDEX feed_session_subj_restraint_id ON feed_session USING btree (subj_restraint_id);
 2   DROP INDEX public.feed_session_subj_restraint_id;
       public         feeding_app    false    213            	           1259    17083    feed_setup_created_by_id    INDEX     Q   CREATE INDEX feed_setup_created_by_id ON feed_setup USING btree (created_by_id);
 ,   DROP INDEX public.feed_setup_created_by_id;
       public         feeding_app    false    215            	           1259    17084    feed_setup_experiment_id    INDEX     Q   CREATE INDEX feed_setup_experiment_id ON feed_setup USING btree (experiment_id);
 ,   DROP INDEX public.feed_setup_experiment_id;
       public         feeding_app    false    215            	           1259    17085    feed_side_created_by_id    INDEX     O   CREATE INDEX feed_side_created_by_id ON feed_side USING btree (created_by_id);
 +   DROP INDEX public.feed_side_created_by_id;
       public         feeding_app    false    217            	           1259    17086    feed_sonochannel_crystal1_id    INDEX     Y   CREATE INDEX feed_sonochannel_crystal1_id ON feed_sonochannel USING btree (crystal1_id);
 0   DROP INDEX public.feed_sonochannel_crystal1_id;
       public         feeding_app    false    219            		           1259    17087    feed_sonochannel_crystal2_id    INDEX     Y   CREATE INDEX feed_sonochannel_crystal2_id ON feed_sonochannel USING btree (crystal2_id);
 0   DROP INDEX public.feed_sonochannel_crystal2_id;
       public         feeding_app    false    219            	           1259    17088    feed_sonochannel_unit_id    INDEX     Q   CREATE INDEX feed_sonochannel_unit_id ON feed_sonochannel USING btree (unit_id);
 ,   DROP INDEX public.feed_sonochannel_unit_id;
       public         feeding_app    false    219            	           1259    17089    feed_sonosensor_axisdepth_id    INDEX     Y   CREATE INDEX feed_sonosensor_axisdepth_id ON feed_sonosensor USING btree (axisdepth_id);
 0   DROP INDEX public.feed_sonosensor_axisdepth_id;
       public         feeding_app    false    220            	           1259    17090 &   feed_sonosensor_location_controlled_id    INDEX     m   CREATE INDEX feed_sonosensor_location_controlled_id ON feed_sonosensor USING btree (location_controlled_id);
 :   DROP INDEX public.feed_sonosensor_location_controlled_id;
       public         feeding_app    false    220            	           1259    17091    feed_strainchannel_sensor_id    INDEX     Y   CREATE INDEX feed_strainchannel_sensor_id ON feed_strainchannel USING btree (sensor_id);
 0   DROP INDEX public.feed_strainchannel_sensor_id;
       public         feeding_app    false    222            	           1259    17092    feed_strainchannel_unit_id    INDEX     U   CREATE INDEX feed_strainchannel_unit_id ON feed_strainchannel USING btree (unit_id);
 .   DROP INDEX public.feed_strainchannel_unit_id;
       public         feeding_app    false    222            	           1259    17093    feed_study_created_by_id    INDEX     Q   CREATE INDEX feed_study_created_by_id ON feed_study USING btree (created_by_id);
 ,   DROP INDEX public.feed_study_created_by_id;
       public         feeding_app    false    225            	           1259    17094    feed_studyprivate_created_by_id    INDEX     _   CREATE INDEX feed_studyprivate_created_by_id ON feed_studyprivate USING btree (created_by_id);
 3   DROP INDEX public.feed_studyprivate_created_by_id;
       public         feeding_app    false    227            !	           1259    17095    feed_studyprivate_study_id    INDEX     U   CREATE INDEX feed_studyprivate_study_id ON feed_studyprivate USING btree (study_id);
 .   DROP INDEX public.feed_studyprivate_study_id;
       public         feeding_app    false    227            "	           1259    17096    feed_subject_created_by_id    INDEX     U   CREATE INDEX feed_subject_created_by_id ON feed_subject USING btree (created_by_id);
 .   DROP INDEX public.feed_subject_created_by_id;
       public         feeding_app    false    229            %	           1259    17097    feed_subject_study_id    INDEX     K   CREATE INDEX feed_subject_study_id ON feed_subject USING btree (study_id);
 )   DROP INDEX public.feed_subject_study_id;
       public         feeding_app    false    229            &	           1259    17098    feed_subject_taxon_id    INDEX     K   CREATE INDEX feed_subject_taxon_id ON feed_subject USING btree (taxon_id);
 )   DROP INDEX public.feed_subject_taxon_id;
       public         feeding_app    false    229            '	           1259    17099    feed_taxon_created_by_id    INDEX     Q   CREATE INDEX feed_taxon_created_by_id ON feed_taxon USING btree (created_by_id);
 ,   DROP INDEX public.feed_taxon_created_by_id;
       public         feeding_app    false    231            *	           1259    17100    feed_trial_behavior_primary_id    INDEX     ]   CREATE INDEX feed_trial_behavior_primary_id ON feed_trial USING btree (behavior_primary_id);
 2   DROP INDEX public.feed_trial_behavior_primary_id;
       public         feeding_app    false    233            +	           1259    17101    feed_trial_created_by_id    INDEX     Q   CREATE INDEX feed_trial_created_by_id ON feed_trial USING btree (created_by_id);
 ,   DROP INDEX public.feed_trial_created_by_id;
       public         feeding_app    false    233            .	           1259    17102    feed_trial_session_id    INDEX     K   CREATE INDEX feed_trial_session_id ON feed_trial USING btree (session_id);
 )   DROP INDEX public.feed_trial_session_id;
       public         feeding_app    false    233            /	           1259    17103    feed_unit_created_by_id    INDEX     O   CREATE INDEX feed_unit_created_by_id ON feed_unit USING btree (created_by_id);
 +   DROP INDEX public.feed_unit_created_by_id;
       public         feeding_app    false    235            4	           2606    17104 $   auth_group_permissions_group_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_fkey FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;
 e   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_group_id_fkey;
       public       feeding_app    false    142    140    2148            5	           2606    17109 )   auth_group_permissions_permission_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;
 j   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_permission_id_fkey;
       public       feeding_app    false    142    146    2160            6	           2606    17114    auth_message_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY auth_message
    ADD CONSTRAINT auth_message_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 P   ALTER TABLE ONLY public.auth_message DROP CONSTRAINT auth_message_user_id_fkey;
       public       feeding_app    false    148    2162    144            8	           2606    17119    auth_user_groups_group_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_fkey FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;
 Y   ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_group_id_fkey;
       public       feeding_app    false    149    140    2148            9	           2606    17124    auth_user_groups_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 X   ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_user_id_fkey;
       public       feeding_app    false    2162    149    148            :	           2606    17129 -   auth_user_user_permissions_permission_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;
 r   ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permissions_permission_id_fkey;
       public       feeding_app    false    2160    152    146            ;	           2606    17134 '   auth_user_user_permissions_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 l   ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permissions_user_id_fkey;
       public       feeding_app    false    148    152    2162            ?	           2606    17139    bin_id_refs_id_f3da2fb    FK CONSTRAINT     �   ALTER TABLE ONLY explorer_trialinbucket
    ADD CONSTRAINT bin_id_refs_id_f3da2fb FOREIGN KEY (bin_id) REFERENCES explorer_bucket(id) DEFERRABLE INITIALLY DEFERRED;
 W   ALTER TABLE ONLY public.explorer_trialinbucket DROP CONSTRAINT bin_id_refs_id_f3da2fb;
       public       feeding_app    false    2187    161    163            h	           2606    17144    channel_ptr_id_refs_id_20659dd9    FK CONSTRAINT     �   ALTER TABLE ONLY feed_kinematicschannel
    ADD CONSTRAINT channel_ptr_id_refs_id_20659dd9 FOREIGN KEY (channel_ptr_id) REFERENCES feed_channel(id) DEFERRABLE INITIALLY DEFERRED;
 `   ALTER TABLE ONLY public.feed_kinematicschannel DROP CONSTRAINT channel_ptr_id_refs_id_20659dd9;
       public       feeding_app    false    2206    199    173            _	           2606    17149    channel_ptr_id_refs_id_4224fdcf    FK CONSTRAINT     �   ALTER TABLE ONLY feed_forcechannel
    ADD CONSTRAINT channel_ptr_id_refs_id_4224fdcf FOREIGN KEY (channel_ptr_id) REFERENCES feed_channel(id) DEFERRABLE INITIALLY DEFERRED;
 [   ALTER TABLE ONLY public.feed_forcechannel DROP CONSTRAINT channel_ptr_id_refs_id_4224fdcf;
       public       feeding_app    false    173    2206    194            X	           2606    17154 '   channel_ptr_id_refs_id_654feb30d9ef2f00    FK CONSTRAINT     �   ALTER TABLE ONLY feed_eventchannel
    ADD CONSTRAINT channel_ptr_id_refs_id_654feb30d9ef2f00 FOREIGN KEY (channel_ptr_id) REFERENCES feed_channel(id) DEFERRABLE INITIALLY DEFERRED;
 c   ALTER TABLE ONLY public.feed_eventchannel DROP CONSTRAINT channel_ptr_id_refs_id_654feb30d9ef2f00;
       public       feeding_app    false    2206    190    173            �	           2606    17159    channel_ptr_id_refs_id_7b56dbf0    FK CONSTRAINT     �   ALTER TABLE ONLY feed_strainchannel
    ADD CONSTRAINT channel_ptr_id_refs_id_7b56dbf0 FOREIGN KEY (channel_ptr_id) REFERENCES feed_channel(id) DEFERRABLE INITIALLY DEFERRED;
 \   ALTER TABLE ONLY public.feed_strainchannel DROP CONSTRAINT channel_ptr_id_refs_id_7b56dbf0;
       public       feeding_app    false    222    173    2206            n	           2606    17164    channel_ptr_id_refs_id_890e2a8    FK CONSTRAINT     �   ALTER TABLE ONLY feed_pressurechannel
    ADD CONSTRAINT channel_ptr_id_refs_id_890e2a8 FOREIGN KEY (channel_ptr_id) REFERENCES feed_channel(id) DEFERRABLE INITIALLY DEFERRED;
 ]   ALTER TABLE ONLY public.feed_pressurechannel DROP CONSTRAINT channel_ptr_id_refs_id_890e2a8;
       public       feeding_app    false    173    204    2206            7	           2606    17169     content_type_id_refs_id_728de91f    FK CONSTRAINT     �   ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT content_type_id_refs_id_728de91f FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;
 Z   ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT content_type_id_refs_id_728de91f;
       public       feeding_app    false    156    146    2180            >	           2606    17174    created_by_id_refs_id_28a87459    FK CONSTRAINT     �   ALTER TABLE ONLY explorer_bucket
    ADD CONSTRAINT created_by_id_refs_id_28a87459 FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 X   ALTER TABLE ONLY public.explorer_bucket DROP CONSTRAINT created_by_id_refs_id_28a87459;
       public       feeding_app    false    148    2162    161            s	           2606    17179    created_by_id_refs_id_2f49f056    FK CONSTRAINT     �   ALTER TABLE ONLY feed_proximaldistalaxis
    ADD CONSTRAINT created_by_id_refs_id_2f49f056 FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 `   ALTER TABLE ONLY public.feed_proximaldistalaxis DROP CONSTRAINT created_by_id_refs_id_2f49f056;
       public       feeding_app    false    207    148    2162            A	           2606    17184 &   created_by_id_refs_id_3063fe78c5ceb76a    FK CONSTRAINT     �   ALTER TABLE ONLY feed_ageunit
    ADD CONSTRAINT created_by_id_refs_id_3063fe78c5ceb76a FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 ]   ALTER TABLE ONLY public.feed_ageunit DROP CONSTRAINT created_by_id_refs_id_3063fe78c5ceb76a;
       public       feeding_app    false    165    148    2162            �	           2606    17189    created_by_id_refs_id_427d3b50    FK CONSTRAINT     �   ALTER TABLE ONLY feed_unit
    ADD CONSTRAINT created_by_id_refs_id_427d3b50 FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 R   ALTER TABLE ONLY public.feed_unit DROP CONSTRAINT created_by_id_refs_id_427d3b50;
       public       feeding_app    false    2162    148    235            m	           2606    17194    created_by_id_refs_id_5e091769    FK CONSTRAINT     �   ALTER TABLE ONLY feed_mediallateralaxis
    ADD CONSTRAINT created_by_id_refs_id_5e091769 FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 _   ALTER TABLE ONLY public.feed_mediallateralaxis DROP CONSTRAINT created_by_id_refs_id_5e091769;
       public       feeding_app    false    148    202    2162            B	           2606    17199    created_by_id_refs_id_eafc148    FK CONSTRAINT     �   ALTER TABLE ONLY feed_anatomicallocation
    ADD CONSTRAINT created_by_id_refs_id_eafc148 FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 _   ALTER TABLE ONLY public.feed_anatomicallocation DROP CONSTRAINT created_by_id_refs_id_eafc148;
       public       feeding_app    false    2162    148    167            <	           2606    17204 %   django_admin_log_content_type_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_fkey FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;
 `   ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_content_type_id_fkey;
       public       feeding_app    false    156    154    2180            =	           2606    17209    django_admin_log_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 X   ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_user_id_fkey;
       public       feeding_app    false    154    148    2162            C	           2606    17214 -   feed_anteriorposterioraxis_created_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_anteriorposterioraxis
    ADD CONSTRAINT feed_anteriorposterioraxis_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 r   ALTER TABLE ONLY public.feed_anteriorposterioraxis DROP CONSTRAINT feed_anteriorposterioraxis_created_by_id_fkey;
       public       feeding_app    false    2162    169    148            D	           2606    17219     feed_behavior_created_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_behavior
    ADD CONSTRAINT feed_behavior_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 X   ALTER TABLE ONLY public.feed_behavior DROP CONSTRAINT feed_behavior_created_by_id_fkey;
       public       feeding_app    false    171    2162    148            E	           2606    17224    feed_channel_created_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_channel
    ADD CONSTRAINT feed_channel_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 V   ALTER TABLE ONLY public.feed_channel DROP CONSTRAINT feed_channel_created_by_id_fkey;
       public       feeding_app    false    2162    173    148            F	           2606    17229    feed_channel_setup_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_channel
    ADD CONSTRAINT feed_channel_setup_id_fkey FOREIGN KEY (setup_id) REFERENCES feed_setup(id) DEFERRABLE INITIALLY DEFERRED;
 Q   ALTER TABLE ONLY public.feed_channel DROP CONSTRAINT feed_channel_setup_id_fkey;
       public       feeding_app    false    173    2307    215            G	           2606    17234 "   feed_channellineup_channel_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_channellineup
    ADD CONSTRAINT feed_channellineup_channel_id_fkey FOREIGN KEY (channel_id) REFERENCES feed_channel(id) DEFERRABLE INITIALLY DEFERRED;
 _   ALTER TABLE ONLY public.feed_channellineup DROP CONSTRAINT feed_channellineup_channel_id_fkey;
       public       feeding_app    false    2206    175    173            H	           2606    17239 %   feed_channellineup_created_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_channellineup
    ADD CONSTRAINT feed_channellineup_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 b   ALTER TABLE ONLY public.feed_channellineup DROP CONSTRAINT feed_channellineup_created_by_id_fkey;
       public       feeding_app    false    2162    175    148            I	           2606    17244 "   feed_channellineup_session_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_channellineup
    ADD CONSTRAINT feed_channellineup_session_id_fkey FOREIGN KEY (session_id) REFERENCES feed_session(id) DEFERRABLE INITIALLY DEFERRED;
 _   ALTER TABLE ONLY public.feed_channellineup DROP CONSTRAINT feed_channellineup_session_id_fkey;
       public       feeding_app    false    175    2302    213            J	           2606    17249 !   feed_depthaxis_created_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_depthaxis
    ADD CONSTRAINT feed_depthaxis_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 Z   ALTER TABLE ONLY public.feed_depthaxis DROP CONSTRAINT feed_depthaxis_created_by_id_fkey;
       public       feeding_app    false    177    148    2162            K	           2606    17254 (   feed_developmentstage_created_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_developmentstage
    ADD CONSTRAINT feed_developmentstage_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 h   ALTER TABLE ONLY public.feed_developmentstage DROP CONSTRAINT feed_developmentstage_created_by_id_fkey;
       public       feeding_app    false    2162    148    179            L	           2606    17259 )   feed_dorsalventralaxis_created_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_dorsalventralaxis
    ADD CONSTRAINT feed_dorsalventralaxis_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 j   ALTER TABLE ONLY public.feed_dorsalventralaxis DROP CONSTRAINT feed_dorsalventralaxis_created_by_id_fkey;
       public       feeding_app    false    2162    148    181            M	           2606    17264 $   feed_eletrodetype_created_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_electrodetype
    ADD CONSTRAINT feed_eletrodetype_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 a   ALTER TABLE ONLY public.feed_electrodetype DROP CONSTRAINT feed_eletrodetype_created_by_id_fkey;
       public       feeding_app    false    2162    183    148            N	           2606    17269 #   feed_emgchannel_channel_ptr_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_emgchannel
    ADD CONSTRAINT feed_emgchannel_channel_ptr_id_fkey FOREIGN KEY (channel_ptr_id) REFERENCES feed_channel(id) DEFERRABLE INITIALLY DEFERRED;
 ]   ALTER TABLE ONLY public.feed_emgchannel DROP CONSTRAINT feed_emgchannel_channel_ptr_id_fkey;
       public       feeding_app    false    185    173    2206            O	           2606    17274 %   feed_emgchannel_emg_filtering_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_emgchannel
    ADD CONSTRAINT feed_emgchannel_emg_filtering_id_fkey FOREIGN KEY (emg_filtering_id) REFERENCES feed_emgfiltering(id) DEFERRABLE INITIALLY DEFERRED;
 _   ALTER TABLE ONLY public.feed_emgchannel DROP CONSTRAINT feed_emgchannel_emg_filtering_id_fkey;
       public       feeding_app    false    186    2232    185            P	           2606    17279    feed_emgchannel_sensor_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_emgchannel
    ADD CONSTRAINT feed_emgchannel_sensor_id_fkey FOREIGN KEY (sensor_id) REFERENCES feed_emgsensor(sensor_ptr_id) DEFERRABLE INITIALLY DEFERRED;
 X   ALTER TABLE ONLY public.feed_emgchannel DROP CONSTRAINT feed_emgchannel_sensor_id_fkey;
       public       feeding_app    false    188    185    2237            R	           2606    17284 $   feed_emgfiltering_created_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_emgfiltering
    ADD CONSTRAINT feed_emgfiltering_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 `   ALTER TABLE ONLY public.feed_emgfiltering DROP CONSTRAINT feed_emgfiltering_created_by_id_fkey;
       public       feeding_app    false    2162    148    186            S	           2606    17289     feed_emgsensor_axisdepth_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_emgsensor
    ADD CONSTRAINT feed_emgsensor_axisdepth_id_fkey FOREIGN KEY (axisdepth_id) REFERENCES feed_depthaxis(id) DEFERRABLE INITIALLY DEFERRED;
 Y   ALTER TABLE ONLY public.feed_emgsensor DROP CONSTRAINT feed_emgsensor_axisdepth_id_fkey;
       public       feeding_app    false    177    2215    188            T	           2606    17294 $   feed_emgsensor_eletrode_type_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_emgsensor
    ADD CONSTRAINT feed_emgsensor_eletrode_type_id_fkey FOREIGN KEY (electrode_type_id) REFERENCES feed_electrodetype(id) DEFERRABLE INITIALLY DEFERRED;
 ]   ALTER TABLE ONLY public.feed_emgsensor DROP CONSTRAINT feed_emgsensor_eletrode_type_id_fkey;
       public       feeding_app    false    188    183    2224            U	           2606    17299 !   feed_emgsensor_sensor_ptr_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_emgsensor
    ADD CONSTRAINT feed_emgsensor_sensor_ptr_id_fkey FOREIGN KEY (sensor_ptr_id) REFERENCES feed_sensor(id) DEFERRABLE INITIALLY DEFERRED;
 Z   ALTER TABLE ONLY public.feed_emgsensor DROP CONSTRAINT feed_emgsensor_sensor_ptr_id_fkey;
       public       feeding_app    false    188    2297    211            W	           2606    17304    feed_emgsetup_setup_ptr_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_emgsetup
    ADD CONSTRAINT feed_emgsetup_setup_ptr_id_fkey FOREIGN KEY (setup_ptr_id) REFERENCES feed_setup(id) DEFERRABLE INITIALLY DEFERRED;
 W   ALTER TABLE ONLY public.feed_emgsetup DROP CONSTRAINT feed_emgsetup_setup_ptr_id_fkey;
       public       feeding_app    false    2307    189    215            Z	           2606    17309 "   feed_experiment_created_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_experiment
    ADD CONSTRAINT feed_experiment_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 \   ALTER TABLE ONLY public.feed_experiment DROP CONSTRAINT feed_experiment_created_by_id_fkey;
       public       feeding_app    false    2162    148    192            [	           2606    17314    feed_experiment_study_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_experiment
    ADD CONSTRAINT feed_experiment_study_id_fkey FOREIGN KEY (study_id) REFERENCES feed_study(id) DEFERRABLE INITIALLY DEFERRED;
 W   ALTER TABLE ONLY public.feed_experiment DROP CONSTRAINT feed_experiment_study_id_fkey;
       public       feeding_app    false    192    225    2332            \	           2606    17319 %   feed_experiment_subj_devstage_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_experiment
    ADD CONSTRAINT feed_experiment_subj_devstage_id_fkey FOREIGN KEY (subj_devstage_id) REFERENCES feed_developmentstage(id) DEFERRABLE INITIALLY DEFERRED;
 _   ALTER TABLE ONLY public.feed_experiment DROP CONSTRAINT feed_experiment_subj_devstage_id_fkey;
       public       feeding_app    false    2218    179    192            ]	           2606    17324    feed_experiment_subject_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_experiment
    ADD CONSTRAINT feed_experiment_subject_id_fkey FOREIGN KEY (subject_id) REFERENCES feed_subject(id) DEFERRABLE INITIALLY DEFERRED;
 Y   ALTER TABLE ONLY public.feed_experiment DROP CONSTRAINT feed_experiment_subject_id_fkey;
       public       feeding_app    false    229    192    2339            d	           2606    17329 $   feed_illustration_created_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_illustration
    ADD CONSTRAINT feed_illustration_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 `   ALTER TABLE ONLY public.feed_illustration DROP CONSTRAINT feed_illustration_created_by_id_fkey;
       public       feeding_app    false    2162    148    197            e	           2606    17334 $   feed_illustration_experiment_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_illustration
    ADD CONSTRAINT feed_illustration_experiment_id_fkey FOREIGN KEY (experiment_id) REFERENCES feed_experiment(id) DEFERRABLE INITIALLY DEFERRED;
 `   ALTER TABLE ONLY public.feed_illustration DROP CONSTRAINT feed_illustration_experiment_id_fkey;
       public       feeding_app    false    192    2246    197            f	           2606    17339    feed_illustration_setup_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_illustration
    ADD CONSTRAINT feed_illustration_setup_id_fkey FOREIGN KEY (setup_id) REFERENCES feed_setup(id) DEFERRABLE INITIALLY DEFERRED;
 [   ALTER TABLE ONLY public.feed_illustration DROP CONSTRAINT feed_illustration_setup_id_fkey;
       public       feeding_app    false    197    2307    215            g	           2606    17344 !   feed_illustration_subject_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_illustration
    ADD CONSTRAINT feed_illustration_subject_id_fkey FOREIGN KEY (subject_id) REFERENCES feed_subject(id) DEFERRABLE INITIALLY DEFERRED;
 ]   ALTER TABLE ONLY public.feed_illustration DROP CONSTRAINT feed_illustration_subject_id_fkey;
       public       feeding_app    false    2339    197    229            t	           2606    17349 !   feed_restraint_created_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_restraint
    ADD CONSTRAINT feed_restraint_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 Z   ALTER TABLE ONLY public.feed_restraint DROP CONSTRAINT feed_restraint_created_by_id_fkey;
       public       feeding_app    false    2162    209    148            u	           2606    17354    feed_sensor_created_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_sensor
    ADD CONSTRAINT feed_sensor_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 T   ALTER TABLE ONLY public.feed_sensor DROP CONSTRAINT feed_sensor_created_by_id_fkey;
       public       feeding_app    false    211    148    2162            v	           2606    17359    feed_sensor_setup_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_sensor
    ADD CONSTRAINT feed_sensor_setup_id_fkey FOREIGN KEY (setup_id) REFERENCES feed_setup(id) DEFERRABLE INITIALLY DEFERRED;
 O   ALTER TABLE ONLY public.feed_sensor DROP CONSTRAINT feed_sensor_setup_id_fkey;
       public       feeding_app    false    211    215    2307            |	           2606    17364    feed_session_created_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_session
    ADD CONSTRAINT feed_session_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 V   ALTER TABLE ONLY public.feed_session DROP CONSTRAINT feed_session_created_by_id_fkey;
       public       feeding_app    false    213    2162    148            }	           2606    17369    feed_session_experiment_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_session
    ADD CONSTRAINT feed_session_experiment_id_fkey FOREIGN KEY (experiment_id) REFERENCES feed_experiment(id) DEFERRABLE INITIALLY DEFERRED;
 V   ALTER TABLE ONLY public.feed_session DROP CONSTRAINT feed_session_experiment_id_fkey;
       public       feeding_app    false    2246    192    213            ~	           2606    17374 #   feed_session_subj_restraint_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_session
    ADD CONSTRAINT feed_session_subj_restraint_id_fkey FOREIGN KEY (subj_restraint_id) REFERENCES feed_restraint(id) DEFERRABLE INITIALLY DEFERRED;
 Z   ALTER TABLE ONLY public.feed_session DROP CONSTRAINT feed_session_subj_restraint_id_fkey;
       public       feeding_app    false    213    209    2289            	           2606    17379    feed_setup_created_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_setup
    ADD CONSTRAINT feed_setup_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 R   ALTER TABLE ONLY public.feed_setup DROP CONSTRAINT feed_setup_created_by_id_fkey;
       public       feeding_app    false    2162    215    148            �	           2606    17384    feed_setup_experiment_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_setup
    ADD CONSTRAINT feed_setup_experiment_id_fkey FOREIGN KEY (experiment_id) REFERENCES feed_experiment(id) DEFERRABLE INITIALLY DEFERRED;
 R   ALTER TABLE ONLY public.feed_setup DROP CONSTRAINT feed_setup_experiment_id_fkey;
       public       feeding_app    false    2246    215    192            �	           2606    17389    feed_side_created_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_side
    ADD CONSTRAINT feed_side_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 P   ALTER TABLE ONLY public.feed_side DROP CONSTRAINT feed_side_created_by_id_fkey;
       public       feeding_app    false    217    2162    148            �	           2606    17394 $   feed_sonochannel_channel_ptr_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_sonochannel
    ADD CONSTRAINT feed_sonochannel_channel_ptr_id_fkey FOREIGN KEY (channel_ptr_id) REFERENCES feed_channel(id) DEFERRABLE INITIALLY DEFERRED;
 _   ALTER TABLE ONLY public.feed_sonochannel DROP CONSTRAINT feed_sonochannel_channel_ptr_id_fkey;
       public       feeding_app    false    219    2206    173            �	           2606    17399 !   feed_sonochannel_crystal1_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_sonochannel
    ADD CONSTRAINT feed_sonochannel_crystal1_id_fkey FOREIGN KEY (crystal1_id) REFERENCES feed_sonosensor(sensor_ptr_id) DEFERRABLE INITIALLY DEFERRED;
 \   ALTER TABLE ONLY public.feed_sonochannel DROP CONSTRAINT feed_sonochannel_crystal1_id_fkey;
       public       feeding_app    false    220    219    2319            �	           2606    17404 !   feed_sonochannel_crystal2_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_sonochannel
    ADD CONSTRAINT feed_sonochannel_crystal2_id_fkey FOREIGN KEY (crystal2_id) REFERENCES feed_sonosensor(sensor_ptr_id) DEFERRABLE INITIALLY DEFERRED;
 \   ALTER TABLE ONLY public.feed_sonochannel DROP CONSTRAINT feed_sonochannel_crystal2_id_fkey;
       public       feeding_app    false    219    2319    220            �	           2606    17409 !   feed_sonosensor_axisdepth_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_sonosensor
    ADD CONSTRAINT feed_sonosensor_axisdepth_id_fkey FOREIGN KEY (axisdepth_id) REFERENCES feed_depthaxis(id) DEFERRABLE INITIALLY DEFERRED;
 [   ALTER TABLE ONLY public.feed_sonosensor DROP CONSTRAINT feed_sonosensor_axisdepth_id_fkey;
       public       feeding_app    false    177    220    2215            �	           2606    17414 "   feed_sonosensor_sensor_ptr_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_sonosensor
    ADD CONSTRAINT feed_sonosensor_sensor_ptr_id_fkey FOREIGN KEY (sensor_ptr_id) REFERENCES feed_sensor(id) DEFERRABLE INITIALLY DEFERRED;
 \   ALTER TABLE ONLY public.feed_sonosensor DROP CONSTRAINT feed_sonosensor_sensor_ptr_id_fkey;
       public       feeding_app    false    220    2297    211            �	           2606    17419     feed_sonosetup_setup_ptr_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_sonosetup
    ADD CONSTRAINT feed_sonosetup_setup_ptr_id_fkey FOREIGN KEY (setup_ptr_id) REFERENCES feed_setup(id) DEFERRABLE INITIALLY DEFERRED;
 Y   ALTER TABLE ONLY public.feed_sonosetup DROP CONSTRAINT feed_sonosetup_setup_ptr_id_fkey;
       public       feeding_app    false    2307    221    215            �	           2606    17424    feed_study_created_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_study
    ADD CONSTRAINT feed_study_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 R   ALTER TABLE ONLY public.feed_study DROP CONSTRAINT feed_study_created_by_id_fkey;
       public       feeding_app    false    225    2162    148            �	           2606    17429 $   feed_studyprivate_created_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_studyprivate
    ADD CONSTRAINT feed_studyprivate_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 `   ALTER TABLE ONLY public.feed_studyprivate DROP CONSTRAINT feed_studyprivate_created_by_id_fkey;
       public       feeding_app    false    227    2162    148            �	           2606    17434    feed_studyprivate_study_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_studyprivate
    ADD CONSTRAINT feed_studyprivate_study_id_fkey FOREIGN KEY (study_id) REFERENCES feed_study(id) DEFERRABLE INITIALLY DEFERRED;
 [   ALTER TABLE ONLY public.feed_studyprivate DROP CONSTRAINT feed_studyprivate_study_id_fkey;
       public       feeding_app    false    2332    225    227            �	           2606    17439    feed_subject_created_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_subject
    ADD CONSTRAINT feed_subject_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 V   ALTER TABLE ONLY public.feed_subject DROP CONSTRAINT feed_subject_created_by_id_fkey;
       public       feeding_app    false    148    2162    229            �	           2606    17444    feed_subject_study_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_subject
    ADD CONSTRAINT feed_subject_study_id_fkey FOREIGN KEY (study_id) REFERENCES feed_study(id) DEFERRABLE INITIALLY DEFERRED;
 Q   ALTER TABLE ONLY public.feed_subject DROP CONSTRAINT feed_subject_study_id_fkey;
       public       feeding_app    false    225    2332    229            �	           2606    17449    feed_subject_taxon_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_subject
    ADD CONSTRAINT feed_subject_taxon_id_fkey FOREIGN KEY (taxon_id) REFERENCES feed_taxon(id) DEFERRABLE INITIALLY DEFERRED;
 Q   ALTER TABLE ONLY public.feed_subject DROP CONSTRAINT feed_subject_taxon_id_fkey;
       public       feeding_app    false    2344    229    231            �	           2606    17454    feed_taxon_created_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_taxon
    ADD CONSTRAINT feed_taxon_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 R   ALTER TABLE ONLY public.feed_taxon DROP CONSTRAINT feed_taxon_created_by_id_fkey;
       public       feeding_app    false    231    148    2162            �	           2606    17459 #   feed_trial_behavior_primary_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_trial
    ADD CONSTRAINT feed_trial_behavior_primary_id_fkey FOREIGN KEY (behavior_primary_id) REFERENCES feed_behavior(id) DEFERRABLE INITIALLY DEFERRED;
 X   ALTER TABLE ONLY public.feed_trial DROP CONSTRAINT feed_trial_behavior_primary_id_fkey;
       public       feeding_app    false    2203    171    233            �	           2606    17464    feed_trial_created_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_trial
    ADD CONSTRAINT feed_trial_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 R   ALTER TABLE ONLY public.feed_trial DROP CONSTRAINT feed_trial_created_by_id_fkey;
       public       feeding_app    false    148    2162    233            �	           2606    17469    feed_trial_session_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY feed_trial
    ADD CONSTRAINT feed_trial_session_id_fkey FOREIGN KEY (session_id) REFERENCES feed_session(id) DEFERRABLE INITIALLY DEFERRED;
 O   ALTER TABLE ONLY public.feed_trial DROP CONSTRAINT feed_trial_session_id_fkey;
       public       feeding_app    false    213    2302    233            w	           2606    17474    loc_ap_id_refs_id_a92c0c    FK CONSTRAINT     �   ALTER TABLE ONLY feed_sensor
    ADD CONSTRAINT loc_ap_id_refs_id_a92c0c FOREIGN KEY (loc_ap_id) REFERENCES feed_anteriorposterioraxis(id) DEFERRABLE INITIALLY DEFERRED;
 N   ALTER TABLE ONLY public.feed_sensor DROP CONSTRAINT loc_ap_id_refs_id_a92c0c;
       public       feeding_app    false    211    169    2200            x	           2606    17479    loc_dv_id_refs_id_6b125ca    FK CONSTRAINT     �   ALTER TABLE ONLY feed_sensor
    ADD CONSTRAINT loc_dv_id_refs_id_6b125ca FOREIGN KEY (loc_dv_id) REFERENCES feed_dorsalventralaxis(id) DEFERRABLE INITIALLY DEFERRED;
 O   ALTER TABLE ONLY public.feed_sensor DROP CONSTRAINT loc_dv_id_refs_id_6b125ca;
       public       feeding_app    false    181    2221    211            y	           2606    17484    loc_ml_id_refs_id_737f959a    FK CONSTRAINT     �   ALTER TABLE ONLY feed_sensor
    ADD CONSTRAINT loc_ml_id_refs_id_737f959a FOREIGN KEY (loc_ml_id) REFERENCES feed_mediallateralaxis(id) DEFERRABLE INITIALLY DEFERRED;
 P   ALTER TABLE ONLY public.feed_sensor DROP CONSTRAINT loc_ml_id_refs_id_737f959a;
       public       feeding_app    false    202    2275    211            z	           2606    17489    loc_pd_id_refs_id_f86a6b1    FK CONSTRAINT     �   ALTER TABLE ONLY feed_sensor
    ADD CONSTRAINT loc_pd_id_refs_id_f86a6b1 FOREIGN KEY (loc_pd_id) REFERENCES feed_proximaldistalaxis(id) DEFERRABLE INITIALLY DEFERRED;
 O   ALTER TABLE ONLY public.feed_sensor DROP CONSTRAINT loc_pd_id_refs_id_f86a6b1;
       public       feeding_app    false    2286    207    211            {	           2606    17494    loc_side_id_refs_id_160342ac    FK CONSTRAINT     �   ALTER TABLE ONLY feed_sensor
    ADD CONSTRAINT loc_side_id_refs_id_160342ac FOREIGN KEY (loc_side_id) REFERENCES feed_side(id) DEFERRABLE INITIALLY DEFERRED;
 R   ALTER TABLE ONLY public.feed_sensor DROP CONSTRAINT loc_side_id_refs_id_160342ac;
       public       feeding_app    false    217    211    2310            �	           2606    17499 '   location_controlled_id_refs_id_3808c16e    FK CONSTRAINT     �   ALTER TABLE ONLY feed_sonosensor
    ADD CONSTRAINT location_controlled_id_refs_id_3808c16e FOREIGN KEY (location_controlled_id) REFERENCES feed_anatomicallocation(id) DEFERRABLE INITIALLY DEFERRED;
 a   ALTER TABLE ONLY public.feed_sonosensor DROP CONSTRAINT location_controlled_id_refs_id_3808c16e;
       public       feeding_app    false    2197    220    167            V	           2606    17504 '   location_controlled_id_refs_id_3820f38d    FK CONSTRAINT     �   ALTER TABLE ONLY feed_emgsensor
    ADD CONSTRAINT location_controlled_id_refs_id_3820f38d FOREIGN KEY (location_controlled_id) REFERENCES feed_anatomicallocation(id) DEFERRABLE INITIALLY DEFERRED;
 `   ALTER TABLE ONLY public.feed_emgsensor DROP CONSTRAINT location_controlled_id_refs_id_3820f38d;
       public       feeding_app    false    167    188    2197            i	           2606    17509 %   sensor_id_refs_sensor_ptr_id_1ef1e073    FK CONSTRAINT     �   ALTER TABLE ONLY feed_kinematicschannel
    ADD CONSTRAINT sensor_id_refs_sensor_ptr_id_1ef1e073 FOREIGN KEY (sensor_id) REFERENCES feed_kinematicssensor(sensor_ptr_id) DEFERRABLE INITIALLY DEFERRED;
 f   ALTER TABLE ONLY public.feed_kinematicschannel DROP CONSTRAINT sensor_id_refs_sensor_ptr_id_1ef1e073;
       public       feeding_app    false    2270    200    199            `	           2606    17514 %   sensor_id_refs_sensor_ptr_id_3235e12d    FK CONSTRAINT     �   ALTER TABLE ONLY feed_forcechannel
    ADD CONSTRAINT sensor_id_refs_sensor_ptr_id_3235e12d FOREIGN KEY (sensor_id) REFERENCES feed_forcesensor(sensor_ptr_id) DEFERRABLE INITIALLY DEFERRED;
 a   ALTER TABLE ONLY public.feed_forcechannel DROP CONSTRAINT sensor_id_refs_sensor_ptr_id_3235e12d;
       public       feeding_app    false    195    194    2256            o	           2606    17519 %   sensor_id_refs_sensor_ptr_id_3c033ce9    FK CONSTRAINT     �   ALTER TABLE ONLY feed_pressurechannel
    ADD CONSTRAINT sensor_id_refs_sensor_ptr_id_3c033ce9 FOREIGN KEY (sensor_id) REFERENCES feed_pressuresensor(sensor_ptr_id) DEFERRABLE INITIALLY DEFERRED;
 d   ALTER TABLE ONLY public.feed_pressurechannel DROP CONSTRAINT sensor_id_refs_sensor_ptr_id_3c033ce9;
       public       feeding_app    false    205    2281    204            �	           2606    17524 %   sensor_id_refs_sensor_ptr_id_58051463    FK CONSTRAINT     �   ALTER TABLE ONLY feed_strainchannel
    ADD CONSTRAINT sensor_id_refs_sensor_ptr_id_58051463 FOREIGN KEY (sensor_id) REFERENCES feed_strainsensor(sensor_ptr_id) DEFERRABLE INITIALLY DEFERRED;
 b   ALTER TABLE ONLY public.feed_strainchannel DROP CONSTRAINT sensor_id_refs_sensor_ptr_id_58051463;
       public       feeding_app    false    223    2327    222            q	           2606    17529    sensor_ptr_id_refs_id_13cc1be2    FK CONSTRAINT     �   ALTER TABLE ONLY feed_pressuresensor
    ADD CONSTRAINT sensor_ptr_id_refs_id_13cc1be2 FOREIGN KEY (sensor_ptr_id) REFERENCES feed_sensor(id) DEFERRABLE INITIALLY DEFERRED;
 \   ALTER TABLE ONLY public.feed_pressuresensor DROP CONSTRAINT sensor_ptr_id_refs_id_13cc1be2;
       public       feeding_app    false    211    205    2297            b	           2606    17534    sensor_ptr_id_refs_id_4b47029d    FK CONSTRAINT     �   ALTER TABLE ONLY feed_forcesensor
    ADD CONSTRAINT sensor_ptr_id_refs_id_4b47029d FOREIGN KEY (sensor_ptr_id) REFERENCES feed_sensor(id) DEFERRABLE INITIALLY DEFERRED;
 Y   ALTER TABLE ONLY public.feed_forcesensor DROP CONSTRAINT sensor_ptr_id_refs_id_4b47029d;
       public       feeding_app    false    211    195    2297            k	           2606    17539    sensor_ptr_id_refs_id_4b965b9b    FK CONSTRAINT     �   ALTER TABLE ONLY feed_kinematicssensor
    ADD CONSTRAINT sensor_ptr_id_refs_id_4b965b9b FOREIGN KEY (sensor_ptr_id) REFERENCES feed_sensor(id) DEFERRABLE INITIALLY DEFERRED;
 ^   ALTER TABLE ONLY public.feed_kinematicssensor DROP CONSTRAINT sensor_ptr_id_refs_id_4b965b9b;
       public       feeding_app    false    2297    211    200            �	           2606    17544    sensor_ptr_id_refs_id_6e2340b2    FK CONSTRAINT     �   ALTER TABLE ONLY feed_strainsensor
    ADD CONSTRAINT sensor_ptr_id_refs_id_6e2340b2 FOREIGN KEY (sensor_ptr_id) REFERENCES feed_sensor(id) DEFERRABLE INITIALLY DEFERRED;
 Z   ALTER TABLE ONLY public.feed_strainsensor DROP CONSTRAINT sensor_ptr_id_refs_id_6e2340b2;
       public       feeding_app    false    2297    223    211            �	           2606    17549    setup_ptr_id_refs_id_20b6d3b4    FK CONSTRAINT     �   ALTER TABLE ONLY feed_strainsetup
    ADD CONSTRAINT setup_ptr_id_refs_id_20b6d3b4 FOREIGN KEY (setup_ptr_id) REFERENCES feed_setup(id) DEFERRABLE INITIALLY DEFERRED;
 X   ALTER TABLE ONLY public.feed_strainsetup DROP CONSTRAINT setup_ptr_id_refs_id_20b6d3b4;
       public       feeding_app    false    224    2307    215            Y	           2606    17554 %   setup_ptr_id_refs_id_6a57c16e919235f4    FK CONSTRAINT     �   ALTER TABLE ONLY feed_eventsetup
    ADD CONSTRAINT setup_ptr_id_refs_id_6a57c16e919235f4 FOREIGN KEY (setup_ptr_id) REFERENCES feed_setup(id) DEFERRABLE INITIALLY DEFERRED;
 _   ALTER TABLE ONLY public.feed_eventsetup DROP CONSTRAINT setup_ptr_id_refs_id_6a57c16e919235f4;
       public       feeding_app    false    215    191    2307            r	           2606    17559    setup_ptr_id_refs_id_6eed7bdc    FK CONSTRAINT     �   ALTER TABLE ONLY feed_pressuresetup
    ADD CONSTRAINT setup_ptr_id_refs_id_6eed7bdc FOREIGN KEY (setup_ptr_id) REFERENCES feed_setup(id) DEFERRABLE INITIALLY DEFERRED;
 Z   ALTER TABLE ONLY public.feed_pressuresetup DROP CONSTRAINT setup_ptr_id_refs_id_6eed7bdc;
       public       feeding_app    false    215    206    2307            c	           2606    17564    setup_ptr_id_refs_id_7d373c91    FK CONSTRAINT     �   ALTER TABLE ONLY feed_forcesetup
    ADD CONSTRAINT setup_ptr_id_refs_id_7d373c91 FOREIGN KEY (setup_ptr_id) REFERENCES feed_setup(id) DEFERRABLE INITIALLY DEFERRED;
 W   ALTER TABLE ONLY public.feed_forcesetup DROP CONSTRAINT setup_ptr_id_refs_id_7d373c91;
       public       feeding_app    false    2307    215    196            l	           2606    17569    setup_ptr_id_refs_id_c7a1f61    FK CONSTRAINT     �   ALTER TABLE ONLY feed_kinematicssetup
    ADD CONSTRAINT setup_ptr_id_refs_id_c7a1f61 FOREIGN KEY (setup_ptr_id) REFERENCES feed_setup(id) DEFERRABLE INITIALLY DEFERRED;
 [   ALTER TABLE ONLY public.feed_kinematicssetup DROP CONSTRAINT setup_ptr_id_refs_id_c7a1f61;
       public       feeding_app    false    215    201    2307            ^	           2606    17574 (   subj_ageunit_id_refs_id_46080b085b967618    FK CONSTRAINT     �   ALTER TABLE ONLY feed_experiment
    ADD CONSTRAINT subj_ageunit_id_refs_id_46080b085b967618 FOREIGN KEY (subj_ageunit_id) REFERENCES feed_ageunit(id) DEFERRABLE INITIALLY DEFERRED;
 b   ALTER TABLE ONLY public.feed_experiment DROP CONSTRAINT subj_ageunit_id_refs_id_46080b085b967618;
       public       feeding_app    false    2194    192    165            @	           2606    17579    trial_id_refs_id_1ed49f9b    FK CONSTRAINT     �   ALTER TABLE ONLY explorer_trialinbucket
    ADD CONSTRAINT trial_id_refs_id_1ed49f9b FOREIGN KEY (trial_id) REFERENCES feed_trial(id) DEFERRABLE INITIALLY DEFERRED;
 Z   ALTER TABLE ONLY public.explorer_trialinbucket DROP CONSTRAINT trial_id_refs_id_1ed49f9b;
       public       feeding_app    false    233    2348    163            Q	           2606    17584    unit_id_refs_id_1888eaa9    FK CONSTRAINT     �   ALTER TABLE ONLY feed_emgchannel
    ADD CONSTRAINT unit_id_refs_id_1888eaa9 FOREIGN KEY (unit_id) REFERENCES feed_unit(id) DEFERRABLE INITIALLY DEFERRED;
 R   ALTER TABLE ONLY public.feed_emgchannel DROP CONSTRAINT unit_id_refs_id_1888eaa9;
       public       feeding_app    false    185    2352    235            �	           2606    17589    unit_id_refs_id_1d21600e    FK CONSTRAINT     �   ALTER TABLE ONLY feed_sonochannel
    ADD CONSTRAINT unit_id_refs_id_1d21600e FOREIGN KEY (unit_id) REFERENCES feed_unit(id) DEFERRABLE INITIALLY DEFERRED;
 S   ALTER TABLE ONLY public.feed_sonochannel DROP CONSTRAINT unit_id_refs_id_1d21600e;
       public       feeding_app    false    235    219    2352            �	           2606    17594    unit_id_refs_id_28d6e274    FK CONSTRAINT     �   ALTER TABLE ONLY feed_strainchannel
    ADD CONSTRAINT unit_id_refs_id_28d6e274 FOREIGN KEY (unit_id) REFERENCES feed_unit(id) DEFERRABLE INITIALLY DEFERRED;
 U   ALTER TABLE ONLY public.feed_strainchannel DROP CONSTRAINT unit_id_refs_id_28d6e274;
       public       feeding_app    false    2352    222    235            p	           2606    17599    unit_id_refs_id_45dba10c    FK CONSTRAINT     �   ALTER TABLE ONLY feed_pressurechannel
    ADD CONSTRAINT unit_id_refs_id_45dba10c FOREIGN KEY (unit_id) REFERENCES feed_unit(id) DEFERRABLE INITIALLY DEFERRED;
 W   ALTER TABLE ONLY public.feed_pressurechannel DROP CONSTRAINT unit_id_refs_id_45dba10c;
       public       feeding_app    false    204    2352    235            j	           2606    17604    unit_id_refs_id_5ff9b5dd    FK CONSTRAINT     �   ALTER TABLE ONLY feed_kinematicschannel
    ADD CONSTRAINT unit_id_refs_id_5ff9b5dd FOREIGN KEY (unit_id) REFERENCES feed_unit(id) DEFERRABLE INITIALLY DEFERRED;
 Y   ALTER TABLE ONLY public.feed_kinematicschannel DROP CONSTRAINT unit_id_refs_id_5ff9b5dd;
       public       feeding_app    false    235    2352    199            a	           2606    17609    unit_id_refs_id_67b8f0eb    FK CONSTRAINT     �   ALTER TABLE ONLY feed_forcechannel
    ADD CONSTRAINT unit_id_refs_id_67b8f0eb FOREIGN KEY (unit_id) REFERENCES feed_unit(id) DEFERRABLE INITIALLY DEFERRED;
 T   ALTER TABLE ONLY public.feed_forcechannel DROP CONSTRAINT unit_id_refs_id_67b8f0eb;
       public       feeding_app    false    235    194    2352            �	   9   x�3�L��ϫ��/-�2�,I-������O�,.)�2�L��+)�L*-�/*����� �.�      �	   O  x�%�A�e!����QPн����Sy�:�	s�ߊ=rmS��_��+����D��gʑ1���e�H�R�4=ц���1Q����#��&��Izi��,i��oڃI�%����ݴ��;���)D۔�cڢ߾Gľ���mڼn�grX�%�����
Xp<?u��#�)��_�כEqk��R���W���-�f��������5w{����^:�����#����(q=}\�Jڗ�R���-K��1���c��B �}d]T����p�S�N�n�AO�;	��<��D�Ǽ��&���i���5������/[�>>2�o��c��_s�      �	      x������ � �      �	   �  x�}Yɒ�6=�_�p"���Y.��*9�*EK�m�T������w���E�=tO/�A:K~��Cw����6��0�I����d!�=��ڍ/��{��`aMcK����$�����6i��֖�F ���Ϲ$�?~����t�����I���x��ώ|�����OJ:>�Y�-�0,׆��V���4.�����>��M\ZWҬ�v07�J;����ٓ�����	|J�F; �ͰV��d�I�K�4`��L�1�d�2c t��|�uz9�?��3i���Ӽ�V4M	���4m
�b�����N���yYs��պ_N�Z��ECbf���b����ϯ�k�6L�$q��0ڠa� �2h$����ҽ������(�b�60�<�Һ�IVbm]���lm�6׊�mq��kE*����нs�U�_��.�ei���RW6��Yd��j���B{�O3��.m�.�M'p��s�i�NA�wN�L�����^r�t�p��*#;T
s�6
�æ��li�G?��a\�����4��_
kZ�`����D����p]�9�$9��^Kk�R!ݰ�`!������Lr��!��@f u`�Pf���4Gk�po�S��k��6YdT�q����}a�������?/I"��ic$@���W82K8i���]��Uғz]V��4��R��4�ES�Z�~Y�f8�ׇ���� |G�;�	���u�#��GL7ä�YE�H)hDJk��8!Z��ִ��_*X��K�`[�qvC�8bpק�=�����Q���/�8���l��I��G1&�2`�(ʄ�al���
4�8�5�tǚ�&؀�Z��kR�t�cz2�@t�&�0��{6��Q��%E]�Yw���<B��{�&��8�-�(�ʀ�0��� ��ţ�<���E��q�|�(⷏����:���p�xF�AWQc�E$B6\��u�/�'3���F�B<Z(F�B
�P�����;I*N��a���&�m&5!$�D�E�n��{x�ero[%ho�c��$һy�5��ɥ��+��y��/I	�O`�K0��D0#Z��'�5�b���Rjw��F5l9���U����Z�����*����׆g
��׆�
\D!�XV�"i]��{���#@���n���'#�I#}5����i\/��e=)Q�����0b��j�	F�_L5A��o�N���1��)��F�"B�r��E��)��W4�V��s�,6�R㘰��˸&,��σ��9=�t5-A��K��H��3$#�[$�͐�F�Ž���+��q���S賮eU����o���?��D���<���������F�w��nL.���˶�u��d�j7�ı�FZ��i��T#M�g E�k$��9Q��f>�E�Z}�M70�(�H�>J8q72�����}#�H/T�%$	U%ig9�K��M�μ0+��M�N�0�әS�����vEJ@��f�+fP�<�s�����A��J���RPD� ���n�n��]o��n�U�_Mi�v�L�2/�������/�|�P���>ܺ맋��������:a��&��ϕYc��.�ke�3�vO���8A٭����k��f�G�_�u��iF����1�5�m���/�e�utC�a��g���f�i�#� �HJ>#eZ�3��_�x����\��z�%n��U[�Rk��T[$�QkR���_]�k�wm��bi��x�qP��D���4M�}�      �	   2  x�uW�r9<C_������'zm�8vw.c�Ll�^�(�=���$ek�~MJ�(��� J�άʪ�z��/�pس�Gj�������Dl��b��wa^�H¨������+닓صܓw��Lr�B.��q�������B���=���;и����~��g��&c�\��]�����]��Y^��*UDJ���[,D�	��K�yù<!�!�v&t/@4ҳ������o���������=���\+��(7Ny{�;iي�q��3��8o,��;*���BR�u45����DM�
<%K�I{_C���ʙ���7�%��7D�M���[=�����1����S��hY�_��i�y����hu��V�):R¤4Ek���.��z��I�z�7 I2@��m�y�~%׍�_��;�.?Y�M��ۮO��(犒����Z=���.���i�}���_a7���\c�=wF��~v[�n(��Sԝ���0l��[:ty�9!K���* Ot�$��){a��މ��$�U�`/�\��_��80O�4��n����T���8>�,w��U�X.�6�<g*���)�P:��L�^T��⧵,�t�׼�S�ݯ�ےWq��~	�"\����i{���qد7T�x��r�P\:iCN��I>��d(��-%y�m��Ӏ��~&e�ÆN�d�N�JT%E��Ǐ؇x�)�i����=c<���G��E:��[�g���x�YD69����)=6%I㒮&T�J����G��	h(z�_9��	�hUB%Y���
RnM�۪�Vo��j�D�6��RC	�y�Up"JE��b16%�����Do�I�s���l�g�p��ڀ�\��(�hEC9l�v�>> ݧ��LSW��g$�9���U0�j�Bx���PU*�@�4��[[�h�tBp��[i��4��}�p���2[b�0���"�
sk����*gX|�[t9X-E���!�i'H���dot�9��Y<k)�t�N�r'<+����v�����K4؇獧��q�/�E��|R�\�(��jT���M������*��M��{���ӭ7L��1��o�Ӱ�������6Ѣ�&��'�}�!)��K��XT�D]2�xřY�S��0��ʈ׉6qƑ�S��mi��=�|�#��|
O�{�ܭ�݅0�cJqA��*W�l��V#q�����q>�7.��j@���iCGL~r\>5oZ�w[x������a��;.7�ն���$�B���Z���l%��l�	u����:a�QW:�S �w"�ōNez=e�e��>�}��9��m��CU^��?���X�Փ�^��W	Z�m!&���׌�����v%���P�a*����~�ޣ�� �m#/�y5�x�B�
3�9(�>�,S	R�H*d�E����A]���0�j�s��n&���cn��?��ޖ-.�1;g�<K�C�jD)������V�%��)�F@s��'�wұ�n�I����2-7���Ɋ�h����b���J��a��<�D*e_��Λ���"\M�MG��䞊���5��8І�W����5h���4���'�RI#��Ǵ�W'kE���F}e��1S�փ$�\�ې.Ƴa)�	-��sش��-�6�!aV|�t� 3羒�\s�)��ґW<�*��,+������t�橭��|9�uc�N�/MT��zO�����tD��V� 5Kj�Pa��@5	�$�F$Y��L9B��m��It��Îk]#ϛ��yv��*����1iO�x�~�`ݗy��e���+0a����$2U>]cM���m'=�u\�>�����������      �	   X   x����@C��G�e���Í�7@H�ێo��J�r!9D��Y(��e�T*�-ǉ[��I�??䒋T���{��@O�      �	   �  x�5��u,;׷��C�����c�S�aQ��%!3Ԩ���{�LM��k��ο����T����0���i45��i~q���)8%�wSS`ښ�+F�-W��[��ω���励�YZ����oi1h-��[Z����oi1�"��[�8|��e�8��F���h�(0F�c�(�e�(�e�(�E�ڈq���=1.�{b\О�'F���hО����������xb�����=���I�Y�Ę�$�$&1fcc&1�0�1`�F�1`�F���1!�#�x`���b<0R�F����˛)�7�˻@Io�&�����.���@Jo�j{�X;<��#h۴ m��m��m��4D(�i�Pn��<�!EyLK<{LCR�|ִ䳦%>�1-�Ɏi�옆4�1q�2y�2��2��2�ʿ ���W��	��� �˯��� �K�A x�:$/���!���_��J�/�	���K!��t+D��Z�ͽ�"�h�nTFӐ�t7��0~%Z-��}�Ѵ����4�<]�4��!��@�a4QO�z�i{�W���)Pm�tU��0�������4F�u̼�"zF0�n�`�]�ܿ���]h9��!�۵���h¿]h:��!��Ձ��nɡ/����;r��9�Ź�|q��_�+)!��q���8���r��\1��犁�>W��i1�ݧ��r��{Zl�i1�����ޞ��-b�E�÷���=#V����3b`aψ�}=#��X�3b�"��ω�5:Ol�yb`��;t�X�����'�<1�?牁�9Ol�yb`yj��ݩ%V��؜Zb`qj����%֦�ؚZb`ij����%V�BlL�X�
1�/b�b�b�b�b�b�b��b������5Y���B��P��+
!���B��#>�N�����;A�M�j�!�6B�m�P�4��iHI��:�AuLCꘖ|ִ䳦AuL��!�1q�c�ReSeSe"Se2Se�Pe�Pe�P_ԑ����X�v䪾�#X�S�S��S��S��S��S��S��S��S��S��S��S��S��S��S��S�_����S���@!�+�B(w �P.
��B�(�rP�"�j���U@!���B(��Pn
�\B�(�r!P�F�ʕ@!�;�B���t��[�B��
�(��b����B��
�(���W�����W����W�����4נ���ů �%(*��E�4W������\��R���R�~L�I���@̺�@ʺ�@Ⱥ�@ƺ��|�P��O��O�HO�O��F�HF��o��-b�E���E?1��~b ��@"���@�y�'F�-b�"F�-b�7>K��,1�������K:K��,1�������:K��,1��b`;'��rN��ݜ�9!6sB,���	1��b`+'��RN����+9)6rR,���I1 �I1 �I1 �I1 �I1 ��b@8�ŀpf���_Pf��/(�����2������G�����l�/|4gy�G�Nz�8'��>�c|4�4�h�i��Ӑ�9�!`S�!aS�!bS�!cS�%�5-��i�gMK>k|4e|4e|4�4�i�i��\Ӑ��� о@��kDj������h�"���k�n\�Ѹ�q�G�6������}@��>7}4��h�	�Ѹ�q+�G�Z��ƽ@���>��4W}4��h\�Ѹ�q=�G�~`����:n�"�qG�G�B�-A�k�>�}�\��sS�G�UA=w}�\��s[�G�uA����`4�n��2��Π��K�>zn��6��ޠ����>zn��ŧ�hq��]�[pu�Z܂����\����������^&��쵸Ww��-�:|����5����F��gE��k�h�~���5�m�L4�����D�	l=�x[O4���W��D�l=ю^&aˆ�%lY�<�����X��K4^�b��sX,�x�%b�D�zV��gE�zV4�"D�U,B4��"D�],B4�"D�e,B4��"D�m,B�&-Dk�B�&-Ek�R�!-E�R�!-E�R�!-E�R�!-E�R�!m����h��-�#m��Hۢ=Ҷh�4m u�Q�G�푶E{��iG4]|�8���,�C�H<N�"�8���,B���H=�wn[�3�en�[��en�[�2�:B_*t��RT�}��)�JR�c���B��+M��W�
���D:J_�*t��RU�0}��i�JV�����B��+]��W�
����:R_+�j���f����&�k&9��a���f9��a�ÍCsE�r��w��ҡ�"��8r];�H�wB�v�B���"\=TX����p�����	E��ʾ���x_����׮亂��HWU鎡�"]2�U�[���t�PW���*r}��w�gaQ���ʊt��Y�.J+�mCkE�n��H���¡�"�84W�+�ꊌ��t(�H���ڡ�"�;�W����t��`��)L���t�n)L���t�n)L���t�n)L���t�n)L���t�n)L���t�n)L���t�n)L���t�n)L���t��o��h\|��[
ө��0��[
ө��0��[
ө��0��[
ө��0��[
ө��0��[
ө��0��[
ө��0��[
ө��0��[
ө��0��[
ө��0��[
ө��0��[
ө��0��[
ө��0��[
ө��0��[
ө��0��[
ө��0��[
ө��0��[
ө��0��[
ө��0��[
ө��0��[
ө��0��[
ө��0��[
ө��0��[
ө��0��[
ө��0���
ӭ��0��
ӵ��0���
ӽ��0��
�Ż�0���
�ͻ�0��
�ջ�0���
��\fr/sʽ�e*w��X�0���a.�����榞77���T�s���Ra;�e>w�ˀ�4�	�i.#��\ft�����r�����W6T��چI�_�0���fy��0o7��]9R�v�Haۥ#���u��)l�w����¶�G
ۮ)l�{����¶�G
ۮ)l���}�r%�|�J�+H
�� ]��KH����2��E�{H��."in�����*�涻H����:�n#in�����>��I��n$in�����N��KI��n%in����ݟO�u1Is��$�mW�4��M��v9Is��$�m�5���~�����&      �	      x��k���&�Y�W(�|��[�xq�nD_�m�}�a{f�7v7�*��t�T��r���/ 慉̔2%�{Nĉ���@A��(����\���^h�2Zk�W�0���v}��q�������/K��;ӧ�j�c2�6��?mn��ns������9�����Ohy.�����C��$m|a��j�	������&@����NIۊ�����׻�~�is����ۺ��_��������VQ��+܈����?-�7�w�n�Y��پ�n�/��$�yi傍��M�z�����JXd�2ɺP1��b�fs{�C>���?�oo77�U�G�J/wﻍ�//�n6/����������E�GZk)�{��
�SV7B�Q!�E�0Bm_�^Ek��:=a�-q(o��W��as����B,c^��
'�9 �=��"R}�eYޮ?mP '�4X��Ӂ����X�!h�yeA�J M�x��د��Մ�^������jM�7�����"��@�PS�b���1�h���<`�n?T�I�"?���{W�si�SO0Ռ�Ka��{e�o�0�R\d�-��*� \Ԧ1�(El�Oc�� �h����4�������*���J����v�!0���B��:X90>�f����b�IљZF��酉+�}R�znij�!�,ah�l�8$��ǃ��DA������$�5��4���w����[2��:(I���U�Iٚi��E�qS�hI_���OC���,�������>�A,��A��H����a�|��}�a�3��t{MT
�wx1�.L���fO���r{���a���r}{����=�ݯ~g���F_#�b��\;�faYc/YX����cS���o�l"+ߧv]�dT�k� 9,0��L ��ܒ��)te���$?v�n�U��$������{�g���v������wNI0�qh�@����4�i	�g\���~�(��ò�Գ���"X6���I��NiW��@$ן���J�+�Ʃ�C��ϰ�����< �d�=a��!5�L4ʺt)R����hY�n�j҂5���zG���>\��������#9E4S�;��;��\|���ڌQ�Ԥ�~� h��0/����q��t' oi�[���P��#@йGC� ��i�0����A\�b��u����on	�Pd��hQ=�8�^-��>X�m�lx~��$y�JKd iy��������f��q�	�5�B�<�^��R�2�������]��v���O���}�?���@MLd���,��e�����f�a{���zH����HY���W?"f��U��*%����4��������q�� #p6Y�^𱆀n�y���O������$`��(�F&����Sw
"�D
d�ѿ�ܱ�Ф���Ҟg���}��'C���Y��^���$�O���:\�SCb�v��`&����ش�c�����Ԏݑ⌾�ج��rW��ͯHm5.�4�qK�lhPw��h>6ÉmL��wX�;���vX��i������<��#��
M^���!�ݨH�*xm�>x
H�I���M1j@����D�T��\�pW?~�H��Oh��;pjd�@T�O�{��ı�"I�sc�W��ԑ(ڙ��R+ZR5Nco|�H,��,~�|z�/��k>}2KG��f/�lxv�(�x`�W� v������~�����WWْ�$�-m�qb%����ǻ�v��i}����|<�$�����M�ŏ�O����jw�ɴ$�Q�9tB*�����)T��7�k:�y�����۫MF1}��2����x�K����Lg�t��r�BBC�o�~ƹ�!9ID�+�$hE�ś_��w�4d�'Ӹ?��%�������QO���Wt��LC���o��S'O�#p�C�*.�r���A�j�����ɞ��u9Z���%d�e�_�,q�}{���Sj�k%�8�}�9���%�^�-� ���t�}�B���)]�2�-�εlRh�H&�0�+�7��L0��*8�jX���Ϸ�_r�9�<N~ܫׂ%�W+&F*?.�I�/,M��>SHE����FmK�
�h��*�&�hS_P����M=��^t��:�T��ut�*��n�k���]���=[-���ܾ_��1��Ί�[�`��5�]���ϛ��M�/��H�M댫ih����~����z,�p�fP�\��^���:�������^o%��m���F�S?�׽��$r� 	�!8t��Y�ۆ&ZE#g�e��^�F���m�o��5��0��_��Ć����]&����~b�]�n�h]�����/�}V+���,0Ղ�%9��t�Jc-�6�I��dxY*'�GC�:Y]ߟ*��/��ƾM��#.p�����⤂!��eڮj(��%������G(�]� t�{�N*�E�.�.����/[�֟�"�z�I^9��m�v��b:�#`��Ɠ��߽V��_��|�,�Tg:�AuF�,/�L	��I�[������o�5p]��t�ך�l�I���~������B'�LJF:Ȱ�V��i����7����Ҡ���~94�
���y�%�Ib��-$�
t*v�>���h��	�+뢭E����n�����g'h��ХXMB�I��"4<����ږ{:�7婽/i���.��,V���>e���O��}եA�Q���R��OwD�sG�㛗��KaL��>"�;��!�����>5/x7��Ơq�'vq,�{ؐ�'�#��l
!6���e����������N �B^:��5ch�/���J)�?�aA������7��������ВupXb�.怋�����^���$��ؘ5�C�rx��e�v����� zT�g���������z���1Q�ѩ�h.F����PtX�7@�}ڶh%y�9�K��V[]�'����/g"Y4��޶mp�9in{���9j���
���<��]$'4�*�7��?5<|�Ǭ���yXtq�3�a��Զ;�)�����R�4�b�ӌ�������N|��H�� �JTlXTs��1�&-y�3��".��,����HF�'�}���Q��j9v[;������a�J�,�*�,����� h���!���h�Q�D����^~Nw)+����sZ������*YmS����/� ��7y���В�E��z:�G���|�-܌8�s�`�p���@$�8,���_�m?,�ӳ* H�y��+\iT�!�d(��<���Z2dPhp\��c��#�L�%D}��>��4�9��C3pk\T���;���L � �qOP.�6���)� uA���lL#��a�wK���&HvJ�6�ճ`5��'@Ops�c��#�f(�)����y������$` �xʘ�*��ma�ZQ%:����D-�m����v�y��t���	��m��$���fw�+G�����jOG��Xj��	�˕nnB��g�`����p魯�;��v������3�s�aTp�$���Ǹ�k�?QoN
�`�J.&[[	CV��j��j���7e,ܟ��>������:7�#}��e������3*������a�$�@�������M��F��_Ohҳ��Y.]tE����tU(X�i>>�'���A=�[-���LV販� K���6�d�k�T���5>��V�:?�A���_��כ;���n��|�PE2s�^��Ja�j9A�v�g���9"���y�����pa�/ ϛh�a�\XE��ua%�62)��$��捋�"cP^`��Q/tXi�ı�����&�)	1\�F2�t��~X��Y+�)���סyFg���̍u}1:�)�&��~ � 8<J9[?{8���3��#��/Ӏ ������]�]c�A9�۫٪�7�������~w�Y~��Q�>?�����ɚ�)G�Wj9��)ɜ#���^�7��<��M��dr��I�"��u-�uC�m�v��}X���\�&�/�9rpZ�df3�c�k���Y
v�wc������hA�ѻz�V����?I�$�1�	S��,����0�� ���    -\P��N���f�#������`�͟�nK�o��w��Yw�7�2�]`F�|i	��0i�7o:����οl�BR�����^��$_]UJD�����l��S^52t�h��K���S�K���+��ôv��'x�&�/��^��Nv66Om��bº�M�S+ځ���8��chbh4�N���]���%��qi�F7�� '0K#O�q}w����?��;
��5�U�oF�Q�V��_�n�+�	|��5�L�F�6�ʘbML��ܑ��')j������:8���FĹ�eđk�X��qT��p�sp��u�<}�Y�A�ҋ��r����v'T�B�P��9�I���o�pO�J�rl�3�
:WK\ϗ��g��57��aԴR��k%n"�	���$\�������}��%�E���y|Ї1�5lA��ȑ��n�OӍ6j
�Y�!��9&�����(���_����+����.Aa���(����ך��z��M�y1hڞ��+�=�K+)�OM��	���>��\~����nw��w����U���q��;O��v�i�8%B������5G ��g���.�v�in G@���S�na�ƅQ��	 ��ջH��ױ�Q��"���@��+�5��b-!��Q>�����?��7��_�PPh�����|sj������K����*�I�#�2EPF��A�����A-����,���ӧ����`�!8Z��Be��&�p0��㱃� ���:���
��L�0\�9E�g]�IX�x�&� �I��u����s�������	B�B�%n����N����s��z8����4ExI���v��֟��.�P2,"���F7A�4�?�PwU8�Ur
R8���AW���i�{��]4*�P��Ay~��)����ʳ�{�Yu(�����\�U���|������7���[��7ى��$"�-��dw����v�Xu����Q��Ys^L�%����×��e�v�hk�BѶ�	�f{z���.����.�џ^������/��ÿ�sz=��5s�4�@���9ƢQ��ϧp4���yaX:s�8���f���ך�q�QY����������p����Xtܡ�w]�B�"�"$�ՄH}!��Q`P<�'��j��m�p�sZȒk-�#gAߧ�Q<��\�ak8�,i�M������������m�5��bL��g�*�f��E�e���-ω����o�	�����3������~��U���_r�� 'ĥg��卶Q�C�D��x�}�l��#����-��.9���T�V����I�M6o���{V�>tBp��Hg3��SQ�Z�)d%��.q�ߍ,9���(��V��Nm��-�Ȳ7��};�ꝸ��B|����T0���i)����FI>�VM�2��v٧
L�FK��%pePw�,�n��������w��ʇ9����F�T������� �z�o��T�ƒ���i7��ե��4�T�b{��m��q#��)UG���ܭ���Om�	�*{�F�/�1�p�Vet#��ƠX$��P�ɁA��ByĨL`�{A9�:}EK#��56�\S���ۇ֕N��5���x��,0aԺh�;i=���L	$}Bs�;ՒK����3�fDyP�1}շ��9_1n� ��VV�T�s�ӫџJ�.��z�We���� �U��녉,rs��-�����c��m�r��/G���c�-�E�<��Ygf�г��Qÿ�X~�Ơ�i�&��3�ˎ��A2���:�־�/�����³!:�&�ۮ��f�N��ͫ��f�<����J��9��(���(<e�-b�2,=m�+�f_�N݀��,���nK4_�ѝL�YR̴�IAӔ�Y��"�ϸ�h�2�Ѧ��N�'�'��%���+�z��<lc���,��G'�G9��D8`����ŉ�\\C��X�G���n�܄���w%�v˸�������D!��2�F|Ȩ<�5)���·���c����p4M�=k�U
�����x�Pb� ���@ݾq���.	:p��0�
�>(Gs����׷�{l��v��~s���(�Ɛw�6ڍ�����/n˜�yW4]���G0RK��г���pd�+9Q8���iT5�V�"�� �Sy��J��Ľ��ZG�5m�آ�dQ��j���H���"��A2ne��a�X���.M��b*6 �c�V�ދXŊ��i��x�\���t����0	B�ȷ������a��K49'3�����ĵr�|omʓx�/��=�km�('���YSX�9�Wt�=?+�%��
�o�0�[`9��w�2|ґ�k������z���_�7W�4�D[��{7��O�͝*�T�d׶E�^�ϩܣ��K���l��[?��z��d\�U��hOj���μ;R�"X�����qf
�`	 ]�j����9a�� h��fPv#�xzB�p�F����w���\k�y���ے�K�^D�U�UNٳ�t�볤�\�Y�mϥY�`��DɅ:wuvǎ�B8���=y�_����s��� �rrV�xy�_}/p�+��*cV&���I0�P��t�Z�G���Q	2*2C�ym40Lvq5Jk�8٪��nt�d8�C���Q̺�����̓ሇ��s����M�s�<T�5m�&) �s�T��e��U�|��_Z#g�1P�ώyȇv>piz�7��0�Um�D�Q�S?(J�A�$%^�mn)�3��G9� �����c�T�&vgN�-�9Xhd�!Њ��N�z%%q�U��#�:Z�1]W�޲길����?�;�+�3��C+,%/o���|����0eڮ��,t�KО���ֈ%u}2lb�S��E��מ\r(N'+j��˯�9*RR��k]}�ך��xm�,@v`���Q����Uo�;˔IRr%�������s�{���>��,��&@C��Ղ�p1<�@hiK�`2�'��?Ƙ���ލ��j@W���3��C��-�SRO�:�����̧:�V*��z��ɝ%nW�,;+tk��no��>�s*)��J.�.P�b��Vq	jҋɣ�A�$qZ �K~g0���j�zU�%G(9�~�P˭�,�pŻ�n'�	�i�z�u�%�����Pޏ�L�������N��`�.�&�G�����p5�#*=r�崜.�U1:���C��A����30&� ����*穎ڜ��� 2�T�R�X��`���p\Tخ|�����e��F���+j�����h$�E���c%��GJ�'wzS7�I�DW�\����8�L'�ǚ:u4����s�T���1�q(ՖQލ)�q-�%��VlUE���'	�h�#��t�s�Ѭ�4�ۭ=.�1e�,1�� �R��ˠdM���m�X;�F�v�
p���$0E������:�CY}�*�*������Jٖ�Y(^�XB�`LHsp�ĉ�鉸�U�z'
��v�s�Ak�_�g��Ϫ�8n�5%(�=��!d����V�e:��6�{.�����\\��/�,��@��6	�Ģ���dZ#h�� O�]t����δV�r9��Ҟ�KZ��$i�H#�T�@�١��J�|c���u�����K�2����4�����B�2m���{�����}��g�(iy��h�S�´��jjꓑ�*g��VT��rvS����o_���ґ�3;�(�urV"Z�Eac�6fZ#h�2�*��pm�ЦL�Q&z'�)����+P���JpKӲ�xz��\o����	J��;iʣY������q����|~f�}��P�\�h�D�'<<�����Q�� ��"h!��0B����Z�ŏ��`�n�RC@QqN�hR�0�>�k��VI����:AvP詫�A�>i�1�Ͳeݣ"�{����J":��f�4�!��~����P�ǟ�q�ZZ:
ڤP���f��y��c;�K�\gC捤�U<Q�	�d�0�a�8����ò�7ǝѭ#缕x�=qo\6�����f��9Tw�y'1Y*֔��}l>x8.g(Q(M(q
�!5���T�J[�    pkB�E�M�:A9� ��ܨ(xբ´�O�� 5<��1�*i����E1������T[�@Ƙ���Q��'*�?�/�X��|��j���X�u�p����+��`ie�����p��5"���C{����p����*Ր��J� G���o'y����w�w'��=���!y�x)
��D�r�sN��Ń4�<�AR�^N}g6dp��|���!JF��>iP6�E#�ԓ��\7������t�����a�VIO�
�[�:�XPנ�ݬ���������#j�76�	m\���R z�F斌+d4��+Υ�Tl���gK\����ϖ�>�7����Tm��u��S+Zس�w�v�cjV~�|�|��Q�0���nTI����K>P�ˤ�;:��?��܁����>ԯ�;���۞.gCm
,����ݞ+����G�m��3~�#�(�;�ZC���}�i2�|��o�e��ᇷ�6N�t���y|�ba8Nt*���\,�����5NҾS��Hտ\�*kuG��[�c��`I���n5h��ᘎ���ա�P��I�lz��W:�`��n����py�]s��������u"�{���^��)Oxǻ\�v�j����}틌�LO4Q��Ŕ���u����	�5KH����O��ʓ���o|���y����ܩz?����^�W:|BS��rz�L��>tCZZIǅN}J*�u��~еHw��lyu�F�����c��3<��x �Yqҟmw�:�_&�8�V�V`W7bƵg������[�z��B>���|�Л���E�*�k)!��i��6�� e%���R�S����R�$ ���) �s7�yd� ���>3����Pss��)�Wpq�&{p,C��Da�t;ڦ(xr��>��o+��!�$Yj~_i�=Ui����i�xۢ�(ZIQP��Us"u���j��8�w��y�x�� ki�,�R�d�*�D��,QVJ��9p�D�9p�*	=���D�r�ҍ���Lz"��du�������\N[�y6��UT��
35r�W1����=l�L�B@#�4Zd�
�*D6Q��Q.cȹW'�q�ꭡ�-ʏGys�^�]^&Mh�+{X���3�a�$>�6	��r}�ˑAfV2~�R���<rE��Q�Z�7w��4xo&3�z�V������8�Ϫ�a�5�RdO7��D7�{I�9�'UO<�v�>n�-�[��ӧ��-��d�>c��$z����,���%:W?P
w^��cƵ{��vTf6�=��q7'��X�^���ۘ�;�j�?�:�E��Z��U��9�@��O�"آ������cI���J#f|n@����?z��0���
�~%uV2�I��_�B�V	�rf��ד��\fI'{�4~�:�$?��G2�-��%?����9�H�zp�[��4s(�>�'8������U�Ĉ7v��Q1�U�؅2&��p7��y�����b���(�8g=��],^�x�3.\��>!��S0�t������:IU�M��	�Z���)�6)J�
f$����ޗY��T4+�W<�|�E�b�����3�U��@��o
���0���.���@y	�i-��(_70��I} >��MAh���8 ��ۗ��8C;ZH+P�8��`�P�������h�"Z L��4���Qh��\�L����A���;(��T�|��Y�d�<4.H�\P���|g�4U�؇Ӛ�^5W-S�H� V���1�؆\T��ǥr`��'U�v'Ǖ�2p\]PjB�J��GErl��e�İ���&yB{��R�*n���	���k"�&���\�'J��p���J�5���J�Y�G��Aiת^u�{\���p�R�֨�<8��H8z��2��1uXY��g�N�"���Λ&�]����p��p�Xg9����� }�?�c���'���y��o���b���r�2�A��|��Б1Ys�c�j/R��g�$�j�����S���6�O��w~�2aW!�èP�DC��-�޿�X��;����9�E����(P�^lYjAuJI�0�OG�N��#t�,-{ۇ�;At��q��I���QTֻ� ���������V�S��p@՗G)�������&�#?��Qێ��3���h�#��(q�3���yOz=KꙤzVtF�4*8z%��Y^�A��
��̦�~��ғK� �}�dG��+����)�7B	�_�77����R���3y�l�G%�i'UEF�X*��������V��h3NyT��r�Rp�龭����e���*U�N����0�����bʞ&V�6�� 2��ÊRA�,T�W��@�j�MN7������xYl��8�J�|i���q
�����b�%��x(HP��@��P=N�}P����n�I�A��F�ětj�N_LdP�P�{�z����>(.[Ƶ�Zgcq-f�(�:y�)zj�ũ��ӓ�i��TF-))A�<z>E[߿�ڢ��%Ϙ�u�^}�PUo�9j����X���:�E~��w[tʛ����A��r����zG5F�KH�z�a};t%�|���f�Q�ހd�pWlm8�-B�>$�Wh���[�=nq6hڙo�|9Z�'�i(F�/
\JY��k���~�'q,���x���2��i���~���������㚳�1e�P�&��\S3�O9<ɭ���X?�E�5���TI�4b��$w��ON��FW)��3{'�#�=���pj���ރ>!2�e�J�9H�,��$���D��8��>�Ч�t%�wd}J�%%��Ny�Ε���w�<c�w��g?&j����=s�	c��?�L)U��'2�DL��f���ǈ�<�	��dD���c���Ѩ*@*���z���hW��r}��_^�E+I�����(��J��hН�m*�L/\u�Çʠ�i.��N՛�
���J���}�78G+������C؛$�/tq^�>�X���9���S��ohO���T!T����P����O�h4����2@�%��z��/`$=���D���j{`�����9��t3�y�R$υ9��fy t"�����t�b�I=}z����]m���7�Cj^��Hw:T�"�!!ABu�J0$�A����U��I �B�ʒIj2��S���W�����rP�kCO�������d�9�p�壞�U_���}��L�*�%���y]�;�R�U\.��^�(�O�!��B_��N�ބ�2+S_i�[|���x�i�|q����GF�$6�)�Z��o�yNg�ݿ���~ǡa:{��5^F�ف�Cq5�
�L�$?O�D�#�-'�ӆv[W?�p�E�
�ӄ�U�(��X(��{�"�L���ڶ�[��$,�Er�
#��W�v��?��8VJ������
Q(��P�]#�r�P�D�t� t#Z�y��f 	�ɾp�B�R�ƍ���ң ��������H1�i���~m��z��q9�>!���Aj382Q>�lj#��|\$x}8�����[J���q{�1�B�< [�>m?F8�fw?Y���֠*H�:ܢ�j^��mɐREi�����	T3�+�,�ꖉ�Q�%�i�,����E��8i�4Aj����*��s�K �^Z� g�z��3�����K
��2+��+���q�Ӡ�����W�� ŕ]��|e��;�*�d!��'�D�Ubl�)�j�<��-%�v1�;L��个jc���L�n�<�w�����]��ar�'��uʨԒk
�"7}r:��=�LmH퇨m�t� �s�Ar�x�+tQ��d��`�\���ĕI69+�� }O�,_c��PA̓A���9�;�>��[$��z��&�F����g���Ti"���ĥ�̟��RQ
���z4R�%��w��3���[z?N�[�ȹwyEv�/ +�0N_)#�hU�T�*�� �k����V�k޼������D�$���C��4����H�3ߧה&�ʏ�4*@�Pt��_�1 � J �،��Ҧ�fK�e�yCw3��W�{tSC}]�bz:�1F    ���8��B�k���(Ws6��`Z�9����*��ƚ�
�)לo��!M��o>�>o�A�v�O����6e�h�Sj�QZ���ÚH2� ����m�&�$ �����V�(�Z�!0/�"�}h�`�`���BS����p�L�b⊲1�4��RHs�8?�U�N3�~� ����9}q�p�w��D�Ĥ���Z;��&�Ta�Z]!�JӚb%?�����)�[���7q�*��1��̘�ξ\�>.��,?���R~z������'s��O��KrKI�`krO���i�t���r�{4�\�(#9�ܦnK��̀��`����z���8���O�q^�q^�q^{�E��!*��хڠ�q���qM�$hO�bK�+��a��	�J�6%(�q����������]�'k��ͷVg�jU�Ew�/K{���h:��`�M�'�'�����M�D�WJ ZP�Z��MC Ck��*�ʵ*��d6�԰oL���u\f���ȍR�6����F�Q?́�9TKȶ z�s^$��WtB���f. �!�+O��$���}��EZ�y���YЭٚy�v<����d�)�R3s�FN���;�N��KR�ߢ����k�E30_oP���l�@��;�э\���;	��tϕ�]��X�TU�$+������n{O��l�fw�{��<\�x~��(���X[�����A���M]X��D��օ�R�8°�'1����U�zaa�4�ZS��{��O۫����Gs�\}��ݾ��x���b������f-��K�T��U���hնWK��5������?��u ���<���ʥE4������K��L��������t��m���x�Vx�z��L���q�!HfT�e�C2I��03�2+́��FɐwR�9M�US��F���.*,�\�z��=Ɏ�jT+��ǜ���C�UBV��%:V�gγ�M��w�_�B�sC��7 gl�v�r�0/���5�3�]5�g�m&�����G�^~Dl��^�� �:�z{�!q�S�����!I�^c���u�=Ӕ�.�7t��? �����*��?lo����|����g��������ejh�r��lL��Z�G:S.���q+�%��=�t��mp+4��D��m4Q�bŊU%<���>���¡G�#]�.N�-q7ȵ�7!
a�����ܕ>���^�5��~C��n��W��7�LP�(�1�ulC[_e|[E;�$@ȁ<)����s��W�fM��.G*N�gCk�u.�H���tr��X搡Q	Z"�h��R:�Dǥ7)e����qS����fI]�]�3�����K�}�?)y`��ϦCq����ɭ�sH�♞gcp}:gV*E[�F��v?�*�$�C>����������9�j��w���[|����y� P0����G�H ��_�����=$+����~��ӟ+�R��p�7��(*A@�(�(�PtRD�s����U���-~Z\U��9��Y��Ǫ�w+Q����Q~�JԹ4]�޼}���v��ߐ��%4h@|��q����f=T�\Dogw�� k��x�f8?���K&�.�4����)��|Wf��Jޜ�d�����W����,��6�-.�tpR�����٫s��o�j�X �����3�l�����ꅤ�8�;�X�O8��F{~ �h�Y����
��"�Nv��j���K�)� ��[���gi�}`�T����"`~���%Ш�$��Q&
Mu������ U�����9���Ɯ�+'e��}	zgˉGw��6<Z��Qɉg��u�:�5��$�%�M�fZo��o�JN3�r�|�4	����/aH<9˨F��wFIO�oWN2ˑ�)(��;ءr�9ͩ9�6֞�,�p���۲�d��yFf��c��}p8YdG�|j����D�N5`�C'��9Wf+�-祏���OBv�J��;A���8�g�����+j��)O���(��d�>ݹ�y�G����n
���9g=�9�Q ��j�;���MN��ȔEC�c�dd�$�g7��7����Ȩ���+���H�@E)_�OG�9��pn�3������L���io@"'��ĝY�'d�	�m���զ���V#�eJ۷:� ��FS�j����w��\��&)��Nu���?z�W4RN"�1Z����L�,&�A�\� Y}�I�J���4�v�Ac��?oo7����^�]�ò�[6�?�?g[hu�=__U��ˠ9����`$�@�b�CU9������h��ෳ��j�شHt2Ο;�9=++\8�lÇ9��D1b��*ht�Λ���&u�\5 ��V�Ya�ц>&�'H�^�0fVm����}x*�q��W�j�$�+��bg1i4��ߚ/��a4�/��d�7��O�
�?���G��Ok:�g�r�/"�Cq�+}�'��l8�>%p�&ϙ>0�=BL����;�=�xg%�|�H���<>�cYqr}N�+4�*}w6�2��^�
z;�c��͛�d\��V����>�3�#���UP+1�6:I�3/���!xu.��rJ[.ZRP���vtE�,%[	��؀Kڿ�|����IJ����T�"I'��>[oRR��������������2��E%0u>h)�'Bg�:���Rtu[6�H�H������;l�R�*��S`����"h�C�E��O���͗;���q���������^�y�����o��i{}�׻��c�����⇏�ϕ>���J�lo�3�Ê������E ş6����/���@p��\6׃6e�����L,H�1�%ً�؇�v�`�/���º��tA��t���*� �l$L�����A�,#sP��^I��c���V`��(iWp[	����n�2(��'4Wp��U�!�39��TU�9)�1�7���������#�����+���s�]\�4�&tַ��v��,qwY�pr�pm�u^>
�r�ͯw9
*z�$�#J{Hu�������\VϾ�,�["�^BD�sZŦ,0r��"j�Ǘ�<��׷����~��2b�����l۾NTB ��);�� E �R����g�4��$yP��ʣ�q�zpg�#���f�����Y�қX��΅P-z�B�yN�w����$�w7Zg�o��� Q3���3�9�AjT~��pp�T1��8?��FSHLT:�69�Fg��c��$D�Zʩ�p�T]���Iڧ�͚�-
S�Q��ir5Me���9�,�@޶�c��i<�:��4��"��D�� 5�pҥ�+����I bT����~�
�<@D����ѪXH0�F F# ,%�X�I&G)d��< 1���&:�<& �@�ˇ6���VѢd��E�~�?�q�9�w�o"�F���7>��y����P���?���c����R�/��$5?�9����(�%U���P�ӓ���[�c��Kr2��р6X?��C����4"T��`����/�����}��~�~++���-�A���ǚ��&T��uԊ$i)E+��J1�D{I�C
��t�ɺs<�A���X�#���N���������������r�zT2+%�������'���\_tJ`��?k�8���yGD.7:���rtȸV� �oG��*�<Y'���^8b~�n8�,U?�~?XJ��]<g��4���)V6�E٤��<!)8��R&�����#L:(&���<�"�z����R�H76�FsV�x`uI~�j���������5�&
ܻd�*m~D7kJ�Aɰ�+l7:�%�HN�ⷵq��S���U����큟F��s�豟F�^��z\��,��\<ye_i�[7�+�y�7���J�R�c�e�v'����M�t�b͂�|��9��~?!�C�\��������2�����x�,��O9���ڄ͡t��7Ս4�0��:������=(&��;�Zcm?�
��jtV�!Ў-�pB*�S�ڞ��q�"���|"�͢y�8�)I�p2���bW(�x\ȐdEj�9��U*ԇܑ�~���%��.��i]��M��>����Ε��P�17����4���z�tp5M    <�K�Ij�/<�mKl���5�	У�:Y?�L�("�މg*"2+j~��iT�%7�A�Gj�HMo��P�N&�yLҺ���AvR�L��r�E�S�.Vt��Jb�q�U=�w�q�����?��}�җ�H��d�a�h=�<C��H%��Q=�(;)�j��h�����_~���{7.��Ő��pa��ӵC44RO�2r~[����[{@e�JW���93gT��@i��[�9�,��Nt����Ty�KƲY0ܬ�<{ˁ�I��#dQ}L��L~G&S�XK��T��z��	��,gD`{6((<D]E�V�^�3���TA���U�g�@�3�W����H�t�� �$m��SW2��..pme�l>�+�WZͭ���~D����z=�r�=Ц�~U��<ָ^���k݋��{�ͯ݋��[ ��ʉJbP�p����o圡�dz���QG���{d��'��Y�:8Z:h��t�`c嬠D����A��0��ӄ*�����ȁ�߲~�3�5t���9ϙ]���mAO��! ���8�HY	j(7QPV7�#Z��?_�-3�W�W�sȧo�r�1��S[@~O���K��t�V�#��>���[��`��� ��؛� `,��QI'�LI��\�l�,�7�ў�o�|M�>�3'+(��ٝq_=H|A��_o����?mo���Biy��0mDZ9�WƃPՉ�t��@N�맕�Vq�aLt1��d9����:� g6p�_LS��½q���7����qf(MCΜ�.��K�3<�H�Y,e&�~�����VM`�H�Bw���O3���͠�7tsT}?86��]c`(�%1	���,�@�C��P�jD�J�DZ����[�q�Ny�� ����x�Oܝd��|��T����W�m�>J�E��`,*�w0�04��Q�~Z�ণ�@1� �+@V���"��	u���˹�(-P0E�!,�EE���/�Z}o�r��@�Y�ۂ�������o��������!�BJ>JbNˊ�"�[bt��O��o����$栃h�-s��ū���.M��wh�*w+�>5��T���R��7��F��������W��Sޘ��.p�y�Z�A�������_��H��.#M��-^���j�{��Va�)�>-�1�h:4���+��f��[�v�~���ژT[�~4�tX�B����R��:d�����^��&U}�OmQ9����c����!�t��mk�Qt��}���\�y���\w��E��TD#dz�z��%�أ�3.��[��Ҡ�G�� �#�>n"�	�X� B	@�������C�V@�}~�U�� $��m�L* Lpu������a�*.u3��D�!�T��az��ൄ��Y�s��<��T�c�FӇ���h�ʖۃ-�H��ne��ifS3��x��}j�� L������ˇ�qq����d�K[a����I��>V�?6cU_�h]��:���o��f���!���B�g��9�`�Ȍ���a�[�����0���כ�������ċ����߶����ȉ�dh���ю U�F�#@�[_1�u���l��#���@��E���G5��7������
��4C錔.r�1Eϕ�J�����Hv�i���~��Hj��Zʠ���e���X���������Ba�:�P��u����R�K��d1}�����Y�#��~d���p"Ϯ����" ��I�C�uݴ������-Hn��t��ZF%��@��"����d$t�gC�6����%�Ɏd^d�#G��(��j��L�/5�i��Nm�gf튎��tj�c�3�O��;9���􁨖M
���vp�3BׂpT-n	n�taa �WM�Y���RU6�oU��2h�:���q��@w�Ɔ���,`����zy��ڍ�U�e��l
d�R8A�,�^I��@QQ�l
��*LȕG�6�\�R.�vh���x`u��R�U�J���.r6� Xy����_����M��.2TIJpS8%j�LW��g`�d�U���/�7��{��g}//0�z���L����Ӌ�a�㫷�"nvW�h��V�?��&a�bj2 Q���ׇV�G9jwl���?�Ò�N/7S�Y1%9�����MuE����k3W����s��\ʕ*G*��8Rڋ�}p�m4���)�ӋD@���햋:�$�{Mo.a����Lљz�/$ �hn^�TQ�EU�}�0R�D�5��h��D�B�*/��MN�'�I�g/��"��įt��v�b"x)g5�N)�Z�������ϓ��"���z��ך�I�`�,9�%��2��L1��z�u�uɮ8��ӬL}�u�_~(��i-�q�}�1�D���Ğ�-�'�ʙ�,�4��OB���|�q��1W���SOg�eO��m9�=:�F�q�ǱN��K��c�B�[�s��W����{�Ѣ���G���|�Vo,�7���Mg���z��y�?���HMÓ�_=	��Ҝ���?�#�#�>r�޴7�4���jw�e^�S����v�׆�I�9[ۿ��^I�=�[c��+��=�Zrෲ�CsIv.#8P�Ҋ2^��m�$r1�h��.Ց��'����<����Sz>��/#(~�����֓�;�(x�b�%z)ZTf�i�Ka9S��)�8��x/��7۫�c�,�����8�| �L���,m��Fr��v!��B�7=kb����%�n�Mf��[x�i�OB~�-��j����$(�!������6��l����駾�p�~�h-����h*O��+��O�`���!�u���<K���(��YPp�eU���g�ٮA�|ru|z��7\����O�ֿ�d�M�V$��p���$�ŧ@ �1��������r�v�n}�4����D�8�� �w��̈J6)�+������h�fM���������L���;m��k�;��6R�|������,�2Wp+�\,���ۈ��3G�Hh��3��$�\�9�{�mT�i�=�	�����*C��3�Яw_��
?ʕ�/�(��Jb���L��|C�u�W�;�r1��X+�����P�A2Q.e#E����n�o`u�\����*�h��$���A�k.s���υ��uL���ߩ=ճ�\Q>4�'��~�v��(zh���i/�.#�\j��B����=�p��ٜ�N;���=��L�ɵ9��T����[�@$����N�4�����#��l)o������`�~2�֒�:R�Jzt��N�f�6%А��Aa퍈�=^]Qj�]s7^�Z�M�V���^qi������^)^�i%�������S_�m���^	�����o�ۘ]���*euT_�8��v�~;�amL��&J�w����zvc�l��Z�� NnL>d�t���E3�Y6%�Qa��L�#{?���(�0aL�����Z��6V<D*Kqh����8z=��v�&�W���c/zZ�� WT��O�z�p�촾\�z����۩�EY�ר<��+��/
��]�_+��X�Ei�A���b)������f}��sTe�$e��4S].>��3V����ʦ"�p�Ӽ1�p����P���Qa���suE�Ub%���{�&�����,���^��8�zv_����oP��d��˔6S��Z82� ��v6�\��t�E�v�߈j�T6���l�CTE�����~ws��s��@�`}���@�n�Q�ӖtȗV����s��K&�-���MEc�4�Z�{p�O3�jc%'�K��/fOy�^n�����Oc��T���1�ʎTD �"���j"Λś��uE�;49�Ĭ\&?n�X�`�$��v���w�C��2���������)x��y�VIhO��<e|gBk	͙�P��
�Q�H���^�[���Kg%>P�br�tM�����m�$A�4��e)&)>����s}���2�̑��w)A�����. ����9ʛTY4�]���	jz����g���K	�`�3&����bP[���\�9���ϣE���_����õO*������9����9�����>�o��o��    (�R��U[;�ӈrY��g��_n��m���i�=������7cg���$�����f��}�|�H��e_�Yp+�7������g�8	b�YN��y���vQ��*�I�i��M/�����Φ�N��0��3��U��"v��H�"	Mg/���
dU>Y�<�H:��36v��i�m�m�,�d�tf�e8l�p��O8�ςt��#q!�\dN)��?R�|����X�%����b#b�)����><���7Oex�{��Y�~�y*�)I��gs���S9����t^󟟞�kR����'a-�F���>ʺ��bp�/3�$J�x͡�:I7F��;�al-�-��)����M>�����q����h��=�v`9�U Ľ�jS4��dL�ykR���}�9zFb�Fb�VqF��6͉�^�:Ngc���rl��:�_C�v\:6JX���P��$a�: �����`AI�H��f���-`��C�2n:�Ў\a��XOϽח�JX.�=��j:��6�����壅�4���@����-�����T�J'�;=�8|���)./��ϰQ�:��c'[�T+\˚$��@�P۞�Ӿ;�(s[64�������������n�v��ѫ^�%\�wNQڝ�J�Q���2�7}RJ���s�cr�sI�*9�3|Z���':
���Ʌ�_�e��YD�e(����q�8�0;;p�� �y�Mև:�Ɔ·{���m�vUZS�� �"i{�o�������Mu
�!M�Q��Q`�T�{9���u:����(��<�;*�W��N�o*��'3�����|ŪR<�q�ж�i�V��4~�feƦØ��pq�1UG��X����>g������팝䦨R��}p7aݠ��)�bW���Xk�Z&0[�$���q���L�����-ZGh�����ʢ�`�5�����h��op��U)M�� �w���l}�;z �M�q�˷����78��>���uuv�C��D��u*y7�h�n{u6����;����\�}{=r�s�V���}H��u�����<#����&�B�B�Ȱ���m9��V��)9�j�Z�����"��[��.@ʣ�~@k�Y/13�b��S�u�������i]���,�k锢o7��ӫ� t�sQ�3��:~���%�ץ�S��ucC��;��,�
�X��5/��+E�H���7C�Ó���U�{/�Q_�x���-G�9)��������o�n~$W|��}z������p&5��P�Q�T�:	/�h���*�Dz�[똅��Ż���{$4*��OJY���㰆Im��E��8Gl/!���}��Ls ��t�b�ui�^��@�Y�s�y��:NQ��"'p5%�"Ԃ�:���������=9[r�ml�mr���L�T�ݩd�s�)]G�Z.�8�ھBhg�1�d)��6�34�����#5�xg�Ӟ��lI�6s���&�����'��s�s���i"[���D� ����G�mn"��Tf>�������oo6�k�;��$��ӕ�j�a�p�1 ���Q���6��O���K0.����X���

���xD�B���qp���Y���OU�:����-�`�nO��
��L�UBAA4�OF	 ��������)~pʱ(Mp_� �]G-��F��\̪Ta��Ё�GEnd4��6g���B�s8��$Ӕ��l���$���]x}�h}q��1 	�uF539�f��9���y��yC<*w����Ŀ�?o(:������q��\��t	���
�U�ck8��hF���[���̖[�v�$A�v��]*Gi{$#|� �h��r�拢��������gM3��fR��a��Pwl�*&��p,���ǣ��x1c�����7�l]��.�p&�[FH'!=W�U	�K��Ŏظ#�D���x��t�Gt���j�S���a</��DP��3��GWZ�7��#Z(ь����V�YY˫�F,&#Sl~��@�"�8�p˓ u\3 9���N	T3>�t�*�e8tf����������O2�����FE���ɗ~��2���Ҫ�������B:0�H'!=u�J��xR���������i�@�G�攂�����wHG���Pj��mz�ؠ���?6���VV$-]���w^����]@�TW���X'P?OZ'\���az\Z+��9'��m��Q��~�7�qh��xiS�5�ߖ�Uڡ⦯v��HEt��e~NR�4����C�j^��v���890�u�mh��i*�j2k-Y'����y��9�[?2���o3��!熨��v��d�Fp6츢�iW7p�8�%�e��J dh����ꁤ�z�J�=�0��
�PP�\'��"q��
�9.\E � V��Z�}ߖ]��̴�B�U]GUe�i��Mi]��4�d�q��0pTCF��GA�/� B�Ԓ�O �P�2e�6�L㕤�d��N��agǚ	�$�X��m[�2@WG���*�����
�e}3v�l�����Ʒ�C�<�Tii�I��j���e+�/�%p�6���$"�=z:GB7[�ڥħ,E�׭�e�u���[cN��'� �9��É���������n��|]ҼA�`'���L��Ze�@�j�$x��\T�vˈ����TP
ؐ*491��/F]ߠp"핟�PL�|�ÉS��S��6��-��MC��p,�C��6�����˧�-�?���۳����ۧ�wO���N��O��?N��2���d����V�^7h�o��e��J����������H|�O�l�V�2aIE�GYJ�]s�tt:z��5&�j����Ue���ӡ����O�O��D� ����2syQ":r	��	Gm]��_\K���IK\b򭟉kzg,�B��1~�~;'�g�p�HZ�l�_%մ�.������g\�����V� ��(GT;U�	�AX^砀w��^%�W��tCO����^[`~>��l�T����6�}���u�A���E%�I��f�O.|=��?����5��V�
'�$lq3ܖ׋+�h��@%W��uHyj:v���
�XEܭCq���5mq�`h��H彁:Q�7?Q�b�b�>����}��&c��f #��I�^�	�İ�ӥe2��������W�n���U
B�(��,|��v����~���?���h:�F�r�HćX����*��U��T��iT�Z�Pl;���#� F'1-���7X3���I�z ޵"6ۣrk}�ֆ�P���^(��qu�E�
�d��<��Q�Q����p�J]i�$���Ĥ|��� ��?��pQ�֤��ď�)Fת����&-�r�G!��Z{8��yک�q�i�8�4�|g��=�3ͬҠ9h����$�!�h��M4�ǁ�Yс���5s�<�b�<gb�<_a�tM�:��g�bm���N���13�ɇ�?���&׳vm�N�:���"�@�D�u��0K��c��6X��<��:�e-Rp]PO��t]/뼦�T�F����%5}���;�a~")f��R�+�dw;y1e)V3����ڈ@t�*d;6(Hb��ڵ�Cl�*;E	Ȏ1�Ԯ8z�K3���`V�z�&�������fs���Y��1���1Z<7RZ�q)u�o�1�bII>�s�n�"Z��I� ��D<ٲ�MY����������3X^��`=��Z%=�|�t]u6�#΋���<=�7��(3L~��1���6��6cW���ߴ��yյ� K+e][�����s��X`����&�V \
���KJʑ�
I7�j���|�5��XC�3(�<��J����n��oH�%t�Pi 
�l�-�ڴ9����7 ?����|z���KN��Q�V'N񜲢��n`���J:I�;��,Y/$ĩkm��`�4<@4,����D徰����}��\��Ɔ�*��Rt�7��,��u�*/ )@G� ��]��\!B�)���E�w�HS�$���U,#��Ŭ�w���7Q�r��9�K    ��W݆s�Q�n[��E4��Z-�-e�������(�������ݞ���n���/ ��sJ���O�	�Q^�Sl`\i�][0M���޻u�q$i���_����]�X�_���U���..ɪ��0"1J9�LR�_�f��q�$%rzfZR"�=<��n�]�r��1��"��)����{����a�h��9�1b�V�;��U|KAI!��Iq�j�:FZzY�������r*�]l�YɎ	hHAo��+�@�(}���-j�v�)a����� ٝ�K��	P"��������U�&�5m�g-N��
��<�!����Mt�ÿ|ؠ��mf�q)P0$�ܨ�H����d�����b�Kq\R3>�� >+�xrz9�<�.Z<�1�pM��ҊӬ�Y	��<2�8N�O�ǧ��1M��f3
,d��i�ȴ��[�vB�r�?D�U���Ht˂� ����n��n@�V(6�V��Ϩ�g���X���A��\�㢍�"�v�1�8(�>�����Q��S���P����'h{�^\����@�R�Jj�Ӷ��7����0���Fb�A~�$?ۃ�/��n��{��#���*������������R���n��۷a��!L�t�
+&�k��HV�\!���BO^�x�S�.D���Ver~�	x�[{�0?u�c�p'J�?��?���P 3��i��E�'�: � ��t�e=U�.���.ɫ�1���n|�RT�-a�`Y���-a���1(l^��%JS"T@��m���)��+e(I6XY%]��Jq┙.�,%e��v���&Um�TT�U�Q��V��T�\�̍�Y�M�����Vv2�3C�ʰ��Uh��h�c3,�>�b1�Q�ǘI8�V�-�:�8��Q��	dY͊�SO�����´蜯)���.p8ɱAbW](ڑ�Ԍ~S��y=��ʎ�#
�'I'�
A���}�;g��#��Oed�����xcc��_���'�*��p�5q�Gr>RnIhNd���cR�L�����!1��GjA�0���Fg�ʟ�܃C�ǈ݃�����O�tN��l-��Qj�{iyn
�E���V;�������z.lW�Pyfنik2���;���c`�3�$���2C`�=#d�	�:3�T2�4[���`b_�C�OiE�OC��0�?_YY	`�v�������A���>���O��.��j�p�^i!�o*�1Ra��{Y����P�%s��-F��,C13p��t����?Y��7q}���� N��.�E4}k����8g���─w;�����M�PN���dR�\A�ժN�w>uޙ+O�6���δ�Q��Ҥ�唇~�t-�KEq"Ԋ!E�I�)����p� �-�,όq��|+��+�zBT��Ҡ���e�2�;c��̀�Ӓ�Д�ېnaT/>�����D����7���x��l�uzt�Jx+Q�	�6��	���w��rڌ��N��4�����#V���l���d���3k4��&Oi��P�/e�@8����������כ�_�W�_�h�],��^���r��?��n������ժ�G�=n���Mǭ3��u�#7��N�-t��q�w�B�����Nb4�x�U�=����@��8ő+�D��%2=�
i|I�K��Y����d,� cVN`#�T�)�vVr�M�ҏ���ʕ�g����&C�O��ܼ�(UN� ͊&S����!�}���t��krn)gW4�Z�1f�lhjvhrK�S4�:T	V[�j2����J�h�2�;�u�:�u�lf_U�3!�N%Vw5��l�P�E��(e��!>N��!u<F��'��Wy��u�Fj�wR�WR�s�tګ�����N�y� $����I'�w��I���t�zs�ݓ��ힼ�\���'��� H"&W��-O��ɕ�uSQ)j5�L@�u��=>jߜ�r��$0w[8I�g'I��l�$Au�-�&�γ����y�p��;��=C��PL;g��jG�QB�?O,��;�8�����O�I��Μ�:ulV`�{���hZ���Sd�����˦�uUb*�9!��!�J2���2���uL���x��M[��]vEؓAk*mZ���+nx>:gv?ܯ&�����H�(��3��5����Hx�:zu|����y��z�o��7cᛱ��Xh�O������ay{�D �9�ٝ���]բa�!Lf�m.����]�Ֆ��K��9�03KѿEd�[�~�ug���Q8��oA�ǩ���-��ޟM�}d�9�OB����2�n��Ӣ_��Ω�t#8�ceSj�G�M�Iς4)C��Qܻ�>onS�7���I�ͤ�f�7����Y��nF�N�k���Ѱ��W�� �H5]���e8�j�h�P�GZ���R�9+�h^��:,r�Do�:�+�sǤj��X�X�(��5X��L��O�Չ}�9%���U�V!�Y����4�V��Ul�	R�>���g��&p�$z�t/V�����`������FTeRu4��՜��޷�N�#d]^~��RЧD Ϯ�?�ffA�~*�3�d6��'�ھ��̃��Tnܤȡ���ve���P�	��8ʷ{�Bl� �Ś X��������0ڵWdZ�pa�O	�E�f�L����?F�����)����+���h���a�Ȫ��sӦ]��T�L�`�9��%�B-T���c�d�.:���t��GJ��GΡ��"|�29_���ɉ{@ȃ��{�x��ǵď|n �/�RM�s3ꘉS��9�d�!!P�KϜύ��ֿ��r�z���or�-U>=�!�&�)��P�Y��X ��؏��aj^@=��^�$����LN�v�/�>V��e�����P5���W*���N�B����c��b����_���$�=W%�W*ɿI�o�[�$�܂��B�����n���t�jd�.lI���q�x�f�#���%H����1؊_�D�5��"���x���-.�o'G�2�7�L���ܙJ�Q�b�Ը@�S1]��Ę�'��H�P���j��;!����� �'�Jj�[�����{A��/�9��r�K����3�Y(��wUX,7ҏ�'v6�3OHr�H��a֨ti�_ ��w�ۀ~���7Q9���w�_�X�i?�n��_ Aۋ5aƺ^qÜ�'�`H:���(��r�Nv-�H���)��|�1�iֵ9v��]C����i�Ъ{\�{����u_���g��|1�o����|���g[��an�����7T�y�]�9��K�N��-YC� M�q�lk8���z,)��;㧮1�Zq_.�r�h�OS��`���ݛ ������=/w��)k3��ݽ���a~)8�p���ޡ����B�5�z��J�O�͗}B�#;R��AQ�5�6�Jy+�c��p�7��H����su�&���JP��s	��2�=�VOa���t�;��LV�G0��f�f[�G���7խ���-��tuqlc>*�s�B�F��ڣ$���!��������wۋ�a�L��z[�\&Х\Y�,3u�S���e<0���N�s�^ݺE��\^�A]]#�v$b)�����h`��4a���%p�n{�.�q�ů���� �rz��)�4avn�3���o�~<tBi�l�����3�Q[fd��r�AN~*?�ӹ�A`}:���r�x�`
|��ˋa�8���	������Or�S$W]�Sa$0R덵<�N�O�Y���}ֵ���#f���he�YF��exӂt�4r�)%��x�<`Vg��|�R�c��V+a�vکǔ�VZ.a��`j��� �ޔ��R�u�#���6���:�nmU��U��C���U3�����nFn���G
��d�g#��S�n�Z/�(u� T[�E�oэ���'44���Z'�i|�C1zD �����)G4Ȓ��Jq��A�����WA8b�#7����à6.VL�zbQx7��n��$�t�ʁ%����g�9�r`N�J����";�`s������~�����'�E=�m�I�Wh#X���`+�~OvK    ?f�R3M6�d݁��vs�]�r��\'GQ)[�|Qo��f�>������0��h#��#�u�=]��C����Snz���4*��6T�ڷ�~ֲ��Ds���=9S��]������W@2m�Tl���__��������U�xw氏�y��{���`�}�"c(l%��aҎ�r׉��
���F��sw�
�7o���CS�iDk�a+���!iǦ8I	I���v���Z|�>����(BU�ig�4(��u�є�b\;�2���$��Y������Jy�s6�_��/��m�y�a�5VM?�$��?\n�|���o!��#���I�w�o`-� 4KZO��I����+9A�^���S
����/=7�rض��Xօå5k�����bK�PDVD�τ ���r���t�^	!��2�ɜ�Nˡ�h]D`r�`i��_����#��B+5v0�-�}���F����k�b*i�ܭ��u�)b�1��{���/����%.��B��po�.4ɢ��.dq:�`F	s�B��#+!�+hife>�G�E�ag�?�/.X�~e@������O1o%AV�U'��2A���G���$�j�n��L�L��>��sm3��Z0�xf$�)FҰ��4Y��ٷ�c{�ϻRKX`>�KV�9]�6��
�E�ӵd�IM�VZ�6���l��]B���V�<���	�J�F�|���I�G�Svvss���+ ,XIn	 � ��	�H�S���p���I~����d%�q*�3F�,wH�I��8�n�kځ��M����l���za�`�\�D���C�|�5ʥ����z�c�h��$0Cn����R@‣�����?4��Ѵt 	˕�C��'��w	���VK?�p7G��EQ��
��s"�z�C�� ��,g���}�@C�Y���_�O@�%$]¡�`�����˿nᬚ%�Dc��^�pn?�CSd:La�[�����
aQ�E�-5��Bg>\v���`c������v����4:�\|����q�S�O�	,]M��;鲀��u������d�)^�0�r?@�&�H�S�{�uf�jQh�q��d�.��~d+_�˦'�cfl]=�|:�]L���q�n��'b�YeΒrq�
Ö�V��-�<��7y=\[MX��6(E�Pa`�S2�Ӧϒ�rZiJ�d�����EG2���h�K6rf��_�/�-^�
����|o��h�	:JU�I[֙����t̎�,�k�q	�N����5�xB*� ��м� �|�	�!�5H3-���|��;�|����Ņ%Y�s,7J)��n��w;����e�=S����%��� }���{�Q�����E���O��o�P�U�3�d2��~½[��i�WZ;�����	iME��R㕓��|wfb�[k*7�M,�󰍵�4�����_I�g���w��J
>�S:ϔ �[�4T2��;�M@n5`P>�5 C���ʱ��%8��9���i�y�(��0y�w��������F�(G��7���V��`�]��b�_��oty�ȺK�N8XT�"�m��"$h&�^;G=�2e(�g,]V����ќȑ�-���yw���':�4
�U��f���E�a��Lvnw�D�"X�$W�j�r"b.B�������j�6b�!q�rNh��gN.^�݂��	NIH,�q���P�]Z$����4<����ӳ�������73�]�U�/�-'��V�����	zq��Ş�,��&����;�pO`�<��Q�))SK8,	O;S�.y�yS\�ⲽ�T�r=�w���g��B>����J�}$�ш�����z�]� �Ǐ�d[|2؆�c���`#����("��k"�[�L�(x�ʸ���G���j�,��kJ���K�Eltʚ�aַ����ii����񍕡7	��w����>�pL� ��#��ā��..������eZg�zK��t�25gKc-��6e[�� 7�S�����"z��W�&˪�'B���?�~�,�v���v�!_>$��:c�┾��&­j߾�!X�*u��	��X?7�?����y<{�'��Ϯ�\�.gA���1��`�������mo�����v�U�Q�v �������� [J�?Vip)��N��W�NrV�z'��u�/K�`�8ϸh�g�K�L��;^ѕCN@J����W����3,lC���A�5Y��n����X]��7��:����[�[�+�E���-8��P���S�u�i�ՇQ�El�,b�sW�zO/�a�EU`HX�4hk�	 �^J�Z��W�Yn�ȷE�F�*$�Q���F̪� �vW�Dk�'8��I��d����H��DN�&E���(mI�-q�y܂8�s�4oUMVU�2�sX#1}�m��+�����ܜ
�;��<�۩T���N�:�v*ՙh�S�΄��Jv&��T�S�Z3���Â	�?�������.
����.��JѠ�$�@�&��*��v��ڿ��ܶ�I�Af�r��C?CZuݬB������˿nw����6I�dz�=�}�+�1��[�g�QV,w���U�`�s_[z@�tR{��R���X�1�@�"A( �.&�⺡`�BR
X�V�4&�DU.�
�U>&4S��-�=w��36��8�u�^8����j���Қ�|^sP�±
]%��e�������ד4�gz�{��RQ�e�Ȫ�F��F=�L�<ޡ-?x�}��a{сbd8ea,�+�\
+N>�h���l��K�kr�mz'��F��^^��&�˴q��P�4����*�������K�d��1?�D3���n���+U��ka�t<�vn��y�eEWa���o�a�;3%1�ک�l�-�&/����cV�|g �"9W��QraX&W�͍�)�;�ڕ��Ft��H.J�Ɂ���!׻�D�S"#��{^��'�⟏�>������%>�h��������%*�������mx��Q����	� ;���cx����1Q�)�b~!�����*H��iywwX�����.n�EqXow��.��-����ևw{����4�I��M휌r����w��nww���C'�0��rj�L������3<�ͺ�$��Hs[�X���d����}u^��)�]|�7�ū�fs�����,�
��GE� ��u,�-_]�/�e0-�%��ZG��@DZ�{|���>YVEW��#>.FJ�c{�FÁB��ptmA�W��j� ��*~�ywW���n����:�Z?+zK��*��wU,��^�_LOi�T��Ӳ��J������zԔ�b#�6�-�������n�l����XBD�Jh�,Z�R�uYr��׷o9GɅR		�ȚY�[HLV��p�L��L�b��g�i"4�br���T�y6� c�r�nC|��-=jƕ6ɶk?��1�K�q���q�.����旛����7��aw����+�2`+���&2~␀|���V����>p�Mڸ,I)*
#����m�Ԋ>�Qo+�R�7�JΥ��i��k6Ӛ���g:-�Ɨ���)IH�cr���oZI��i	K�P��$��c����R�;�bj�Ѯ����[s��7�i�jO����V���h�z�e��Ώ�닗a��^4(pe��b>�ڶO�mf����VB��$	AX�̌�%2l�z�Q�˕��?�b7�{C�>I2P���~]��W������B�
�w��S�{�s��o��!�Y�
�Qf	�LsQQ�E�O*��<�+x�f��wT�C����;V�x藇�������Ĝ�2J�,��^Tډ<v��0Tb�P�aA��fA�8�o�0T��`�yN��O��;*V��c�e������z�w-1� oh��������U|IKo/"��s`���_�R��#��u_��������������!����5s�L��5v�וqf)S�s���ґ��N�hq<�-9뭶߿I,�@����chs!����n���~�^ӕ)>!}�j    �Щ/���th��ח��b�;��p���]	G�}S��8��]ׯ�8}J��
D��ԉ��D���˥�]�������p��E��$�fi�7��WW����N
�R��nؾ�����]|X_]u>���a4���A}d����=Xa�X�b��x�a&��Ux
s	"=U�o�E���m��i�ң�e�`��&�\c��4�c���=��כ���n��aV��I�Pq6DU�cBoob>O�v��((�!1��T������.�a�y^�z9��$������#��]G9��
���Z�X7w>�m�S���Ğ�sB�U7yI�c��Jq/+�(�����r��//A\���=:S϶�W�ݦ�Ҡ��GS�:�T�v`���e�׸��E����W��Y�K�����_���ܞ4ȱN�S�W�'�ߒ��h��	g� 6އ���]���nʽk�NQ���{��KVPQ#!�NV]>����M_n�u)E�T�);�\*��s/n�-Z�h)0!�,![m�k_�c��e����U�6�Pľ�aw{�<[��������5����������M���aJ���#�ۖ��n�\ɹ�6ˤh��D����2A�����皹N���-&U�`� c�p
��=>���l��]��1|�����H�w���9�S�yt�h9Z�Q�	!x=��/p6��JW���p;�ۏ�?�!�Hv�?nv���+�Kb1�#�2m6����5%D��,4����X��\���SK���N\+vĜc1�<M9�`ґcѧ8��G/m V0�;���_�-C�V��q�:�.6ɷX�k/x܆�V!ǫ5w�w��n�,1�v5���j��y����c7�S��߽[~�r���"��������`�~��֝�t!��c�ͪ�iE_���ʀ����4"g�2g�˺�I��4�;]��������܏6�'I]��O=��>�H���B��r�M�S��,�+��8C��4[�<��0��p�!f��GX�)��;	%X��.�o'�.}E]Vj%�'�O���/���^��?,Ӻ��rARX#�I=��% +	m���i�����Ջ�k*0d���g
�I�r-�bCFi�qm��s��`H����_�X��TH(�^�2���t���+��@RVq��[W�e���FU�J��Y��}�3����T�ﷴ8����6�,�,d�Bѭ�����VJ�G�Cth^���ݡ��"6���@=s/�&G�=�`�ii�<���$+=3��1�}����[���a�+��!�5�����] �3ε�I�2��K�L9[�;Fv�,��}�eD�S���.���b����P&C��Y��S87�ŪY
�4���[W`6��L��il*�qq}�xoxڬ�S�T��x��9!�����"I�AF͘�:���Z��l��?�����㻫ԑ�����}�`�ߗ���UC�㿐ds�rŏ�e�*c���%F�QM9��
i�B�\���Q��6��������VU�������.��gX�f�Pe��~]�g�
���������Զ?�)���R�ɭ�f�/��_FM�AK��e��Kߤ�u(�7�R0+~N�X0\�	��3A�e���3�V�1Y?d�B�>��8g)U��m;p�����;��}��L�9RS�:�c��s������z��JY�w��Z�/n�ﷷ9E�	�������,�DO�i�\�_t"���Rm����gM�v"`(��Ls^J�X뜇7ҳ�>����A�hl�����&=�:��+ɘc.�AO֯��.�������oo%�K���pe���pƊ9i������m�o7�7�4�b �8���i0�����!��96ցiഉ�R���#�u��Ag0%Ӭ��$��xG��
��W}�}�VqO\����(��Y���_��[>>��]�}�xEΰm-�/��æD�gr�[wi�F��F	1|,�-�C�ga����m�W�c���;���cz��z*�mC8^r��.�-�����$.Fe�f�G2Y�d8#��i��=9�:0�m�P��g-'l��a����U���	����C�Ly��3�U�Jb��8wH��\���SL�'�Xb�W�VѺcO�;cu��m�i晫���U|��M�z�UIXol6 ���3���>U82aq�N��b%~r�����K$x���BCE>"�"���|t#���*�u���̳�R�Q�{�Ȥ\Ɨ`1m��jΦ5T�c!�^.S�(R��	
iPy�~c��Á�=�8b�@�)Ds���I:qor��G��l!|B/���F��S� ��BJ��#�&�L`�j K��ŵ����*os�_�w���;l[\�`*���J��6���s���R��p�d��_}�����Ņt葀��F�V��=_k������0]-�;��7���]-3�ǣV+ջ�s��ݛ�j�?,��X漾��fsqwH���g��=C���+l=����;|���_���5���m/�*���FH#�x�����Z�4�r�F�ێS�HC�	��e>F��	J9̥ͨb�<���]��13�"�N�K�z�n�I%�<��ֿ'��Zv9U�Rf%�4q~�m�3w����c���JL˅�ڋ�f�&���	�p+�ʦfH��(���m貈���pM�}�[o��5�]R�YJ'4r(P �P:d��a���>Y^H]�3 s��V�ۥ7{� W�����%�UPp�ǫ+�0s?�ם�C�el��SA���r�@��J��#�6���f�|�&�POş��+#�ɪ��l�Ew��T�E�[`t�{�R����fCI�
2���M���8��?6���H�
3��&w72���Mr�=M�U(�R:cs�攣6��]@�ܼ�\��C����C��6��n�B%B�b�T`a'�z��=m&��غ��������9��}m�vt�0���2jBOŦ㭭B��A�;�ml2��
6,������uʨ��wp�o63��G�1�cTz �/��jyv�����=V:��J&o�!Ύ�Ӝ�?78��M��PI�I����*�2�Ju���Qi�MQM��"��Q�g'�8F%&�@3��&�ߴ������8Yt
�a6��%s��E�E��cT� �1X��It�*vsB���y��^�z�{�� ^	ص5z���I���h�-�m��`�2z�Uh��L�<u�Z��;�4���"<�)ƛX��<�hު����8�O*���ޫ?Y�X@̜���:��r��<@�z�q^%Fĳ�z��˗�<�@^+`[.j�Ą�������q*\�q'����v^[^H�0��K����L��邨2؝褨�R��2"^�P�-(�-u��s0S~4��ۼZ$�q�����y�|���U -1��T�s
!#�s�c*c����5H���a��f��/�T��0���[1���.�nw����x!^�<�.��>�ʺ�H>Y�VW�tiA&F����.ё����M���8~%����q��
�ZPQ�9���'��˝��.�o�u��=I�PPi;O��:�s�7_Pq�C�J�	�7߿�7/��w�lR���R��8K�2�\�d�*�	�~�a%������p>V�	_V�E�BE�M}"7�ȱ�o.Ah�؂TZ�P[(����w�Dqն`���^�U)'�,�)%�� "6�Ri7(�yB�9ID��4���>��Z�Q��i?pp�>O��ɶ����e1P{����O�{��:N�%�G�Ǒ�ڙ���N���������c�ؽHF$Z
��ȀE�@�	.R'��|�x#��(��5�}ސ���|	����Tyv��f���Q��Ƙ��B��������O���݇�]S��e(ΩD�	S�,�wx�� dV��j�c�@�~���H�t��i������5�z�M٬�t�?�.<�El��Ȣ�9��׮h����ւ�������f�4�a���<C��,P(�Hr,�rm
ݻ(x� s0�    n,���(X9�.�y[{I�ڦ�%T�����\�n�����bG�<�1�S�����:W����˩J���V����[T��>�j������U�Q�[pa;���iąrD�}%_�|6u$+�s�2=�H�&�]�ϣ�sԔ��|_>���ъB��}'Q����VRV��"�j�n+��$�e�p9�M��t���:L��/?�.����x$*��p�Ans���M����p��C:NM��w%''��ӷ�&ћ�����fs= ��4ƈ��p�&ͽ�e�O�ZˣH��hX���z����	��i*����4�o+^�h.^���ְ��_.�Րq��؎�k�P\Uo��z�\��X%���H����ӄ�����뻛��zsu�Bf�J��i�7\i9��NMh
1�mp��������)Ay��c0U�BZ��Q�ee�+���L!���4�[Dw��j*�3�PDTi�Ь>�S⚡*���n�
���6̸��۱HH���-��Uĵ�;
[��ҫ��E�����xj�嵡�&T�'S�����Kc�������>L6U.M<6�>�%;x0Gw/��<hnb�����vs��)d�B��a�A�9��6aH���1�7U�g����\��b)i�����B� C�|����_������Q��R�-X���R�?�Q�3oR��)�%�?��f�h�ʖ�*��*���G�rk���vgY�G�0�?j���Qk̵ڏZd6G΢>�5�M$�t!ɤu��n�W,��8GQ���,5턈�;���0MF�7�㎿��a�s�ꔡ��߷7��kx��WqB��d�G�"���i��i,����a,6M�衜�a^��)�ԑ�h�#����HS�(�	�� "��V�P�p(�w�E$�:O�x~6JϞ��R��A���X6/�<�,cf�=&\l��'��.��^ 1li�|��Y�f�r,W6�$��/�:�v�{sa��+l�M.S}c�cC� �k�~��;;l�̶G�`w�0�mHq�z���Tz
�s��9}�S�"sw\aP�I��;��,��EhY�0�ڢ$: ا�( ן���~�)��ל��T�4t���V}^���ɟ�v��?������Wᦖ"EpR�����ɤ�\�Ù�w�W�'@�v.%�^�/ӟ#_ִ @^��`�U����u�Y�騼�Ck�j�Ar���ApX��b���}(^3Rh9���B8WX����Z�X�+��h��⻻��cR9�F��u��l�i�V�|k�0e_ �Q���s��͟��9j�H�������k�Z��?�*� /(_c�^Y0x.�����#��7����w�`��YA�F��`L��ƥ��}3b ���)��~��T�Kd'lq^N����m���>�×;=זSL�S�':n�Bg?�?�k|�����p��c�J��l�_����z�	�E�y�ʠ���B�~[g��/�+�

ǜ�����&lD�����]���Cڀk�SoA�"�j{lJ��%fdn�8�-2-}�
���Ǭ07r|�b����21p���x�Y�h`�it33�.n�W�T��%�@�d��~��\���"�u=Z�~���ߥ���Ŝc�gS���=ml���AQ�τ��Ľ��K@�S�B�[�S�ř#z{�_>����L%������|wB|ps�����2N��E+�I_wF����6vbr&͉��9D'Gq����Cuz�x&��IEϨ)�B����SA��
R�΄ ��bσ��qԌTa(:�=�S�F�'�B�>���i���m�5=��-^��^������ �qj� �c�O��A�4���?\mB�����#�o������)R����rcΝq�r�̬�"�d��]L�G�*%�M�ǚ,���k(N}��Z��RƱ����p�ԊP���Φ��H̰/	�5,pr�]q�Ll���� \�YaD=TR*f�KeͮT�9��Y+�sa!��q+���s�4Y�j�a����i��ﮯ'�k�?^mb��a��6`
��7�����o6��u���v{�x�B,�h'L_�'������6Y�/���煆	��N�ݎ;���M���( 2x����K�=/4�C���jc�\�F�V
��ݻ���,�r7k<%X��s�rp�$[�]�����~�ڢ����.@8)+�U�Qך�鳿��_�����=����ŋ�U^���"��gQh
O��Ƕ��k���Ha���S��.a�
\��7��j�3o�^>\n�> �@L����8�=��}��SG��";K�`���	���q(WR0�̼�_s#^����x�am*�+
�奋�M�[���RWT�VY_��0̻IRT�8sA��F��#]�څ���:�?�A��v���_7{A��-y`fpi��ʞ�ʴ��b��
>�;�2���������PO��gY��t�f�����M��-$�FD��U��_ R|r�e!L �L�IL��9���_n?^�/��}%a�`ډJ��@E�f%8���Du���㟫7*���zA�h�3:��N����"�iW�ϸ'�m���L����eɕtF���WL��]�����1�\@���_�`�=82��z�����������heRݵ�vh(���X�T`�h�湲R8�:�8��8� j�X�}B�;���_�V��8����$Q8	��ks�Z[yPa9콴~��qW��
7�� Su}��_�%NcE���=7	��<�2ux�V���ɈF�ؕ�,�y����c�N<AX
�!^��\�I�eߋhJ8Li��+�f��6aS�n��L��ȥM�哵{��`�xc	bS�
ֱ�::�Qd~޽�������~���+WPl��Șf>��H!m����O��ɒaէ�.nq@1�Vǧ�,={��M�8V���5�;�(W��8}G�|����U���21���,@��,8���������'�_MLZ9���	��<�죡~=��ї�w��C�,i?Wi�	3����O>��Zt4��a��J	�j��~S����������ps�t�w\�T�D����{_d��|ғ1v�F$�ٰ�S���;g�1d�(��e�����l�s1v��?r�kj<rLRcyJ:� ����JM�Ut�$���|%�5�lJy�����QhzJ�že���4�ZT��d��(b `��t,A=�p�\4�k����˂I&��B�|9��'7��6ٔO7��z+���l׿�l.+x@O��$֠K��d+g+R��*��� 
q����ǘ�>v�-q�����K�a�*X�E�1��#v7FcP|1+uߗ,���0�w��;��5���p����6�F^�Eב��I,b����6���vَ'݊3&M5������Is�-���o߆�Q�"üm��>��m, ����}X�����=�M8�x��\>��.9 �u�{�N���b/g�k�(MKŖJf��O��xr�f�^-ҤR��ٕ�2q%��C�ǫ��B�w���b��9��Ս8��P�
��u�J'�|��5�$�%S}�^�	�(e��w���>����LK�[*tB�a���f�Pr�`�&���g���i�t��VKä�����������ۮ=���;��8�"�<���p�������|��G^���D���U��������Ή�B�Y��HU��P�(r6hl� �8��n����䬀��*kd��{�|,�b�׻0�o�.>�TQ��똏�}�X�O�P��Uq
A�y݈4�Q"K]��EK��t�`�κ<[��K�oQ&-�6i~��M��˷������1�'�<����)@�ajX.�`�A~�U��>�Y;+T��*1ֿ� �r��م��5����d�q=���B���zŬ�5���Fw��{G��+��ǡ'�i������v�m�J����զ�[Qy���`-�S��xTO"��a�[�n#p�����$��W���jW�s�gq��������:R��3���6E�aw��h�L�Nᇸ%*�    u0J�����]�E�f�Q�+���;�RW�J~$�WJ�4dq\��oֻ��I������Jk=X������	#�=U)8����i~t���?��1�<�<:L�I,�:��[�p����p���{��)�b��*�ʓ�T��X�xj3�Un�}�.�O�v6t�ihe:������3�A��Hނ6��A�0�Z�8�Wa�Qpݯ�_؆*�]2�*"M�s}]'��C��Z����n��<0r��"!4�D	��)���@a��ikc2#�u|���1B��dy.Í��΅��!�iY�{3�=��ЦiI��Vsnƕx�@��1��E��L[;#�U�+�E�g�0��9SoNŬ+��c��16�T� e\.��no�3�y,�F�	!�3y|q����=NI3q�:tD��H�x>��t5Ay����u&*�}������/�
5�X�)������9�l�ʅ��^z���鹻���$��H�r����#�s�g�|�Jro"�a�
����n���i��^��pOIg���@Ⱦ}|�F0�U���!�&��b�SҒf��1$86�M���YV�m5L�oe簟�%Č^ �(y�W����>�/.�B9ZA�n�������!P��T(+��[��l[Z�_,�J7�R-�a�2��K&� ��vU)�p!Az��_c��HY�s�8����qD�)���g�g�q�W*d�
���Z�sk��-]���%8!�������1��-y�/��R���&�z��s��'FE��d����S�YvGh��쑦�������p%�QG�Q�)�sC����b�6���-
�nqR��Z��b��,D��Z2�7�G��PyWu-�hWK4����\/����=)��X���!�-6$w���⟏�>~�U�������_o���ݭ�h�VD,��(
=`{�!"�=����p(��b�:��pB�}��te!(=z�N5l�9��s����	�|��%U5V�����q���?�6��5���>��/�ȸK�z6�\-�h����G�c��a�7��������(�����S�SY�D�W�W���a�v�ZU9w"B=�;�.{�!*oB��Jq�X�*�QV�9�J����$�dK��Z��$ <d4oh8��;���X[B���+v~E%�
�n��w{�R����Yk����nqJ�/F�q.���G9�A�),ԮB	oG�7�y^Y/�^�Vq��\i�j���i��P��a�V�i.��k�w�7YrH�g���1Ȋ�x�E`��8Q� 
-�L+1/�PM�9CL�����@���Џ�1�a�e��\|*w���4�舀!�M��q t!�b�K,[�'�a3�V,���n����["Ug��Φ���pt!����L���|�پ�f�TV䒴�
��ԢՅ��&\�ʫ�����1�����Cڊ�}���bb�������*ķ�\p\�{�
q�r4�ʖJ�Ň�A�>t!���?�Q��.�z���X�`���*rcKs�b���c�E+�s0�9L��O-J���CXͫ�Zwd1>^� ���v�X/\M�pv��|z,�ҋ���wo����%��*��f�\*�d�[��)��B�5�pV�\&Y�3�����f���̎�3=KV����ux��U9�O�vy('Ouĥ���LA��	K�}>Q*�A��Шż�b?�#V�t�޹���ۂY*�a/��T�ͳ@ƹe�t�qb�|^6�^pX
�)�*�y����n��$،����܁Bh>�����Gm
.q4�yø�h�N�l㹯H�3�"�*�r�ChSI���hM�5���6�K�DBՔ�^��i�E:hD4j£�ȸ�J��ԇ+���t�Uy�p�w&X�Rɰ?�`�Sm���[=@Mx@hҳX�6z셞<}G�X/�����֟e��:�c��X'�6��O��O��|G}<�b�0�������qT[��\c����+vfnU�������9 ��,9��"���;��*	��IBG�h��	V���t��TP��g�rNHɏu����ɿt��'�2���6��`O��*]S؃��
!�c�hqM�����/�0�� oy!U�b��bht.YH�0�UI�]��e�wJʠk�B��t�w��|�29)ߵd!�B񔐞������J'
/��.���*��|q�p�n��s=}bi
�_Ѩ{����P��AmՈ2X��<����Α3�p��??���y�u�E{E
���X����~�O�_�3������&�$�;>�U*��9����)�Q&g@8��A��
��	��"�c�S��Tp"������$
'���T�E����;�-���9Ψ~��z�Ĩ��9:��k@K�)�N�u�V��r�r^I������$)���$�QO'�bd*�bx*��U����<��'N��0�p��"�0ג-���HB��Vh�3p�s�vI�KZH��
8�E��i��@���!S��gm�]�qR����!##���+
I�R�^�s��%a���LS�F߲���t��A��&�waI	;lU҉j��� B��綉�p҅�S]��;��(�n_��&��/F�*E�F��M������?N���#�bK���>�?��IK�N�Y9�g��\UOI�6�ҙQ_A�T3��`,ؿ������m\P%k�|cs�Ε���x.���8��o7�K�.�y�0���ϣi'�
��	xʷ���M-���XC+�]�������M.�����Ֆ��P��
H.
��C����s}��%K��'��2$�2�4�]T(�"ү�i�I�HY(fCr�U�ܒQ1�2ܴ^Ş�
Iz��A]��:�$͢��q�R$Dﷴ�)�ð���Ϛ���O{���i�$%�a~���J�e{ޫ1�%��@G��ש��8��س�N����\қ,XSN�׿��Hz_��Dˈ����; �T�����tb��[�x���a�F��.S�c
��&��\�Iz���Ǿn���+��Ҡ�n���[DлھY�Dmd��N�ʨ� ���L��~X�� �/�ۋۻC�t�^�bʃsc����sYh!W���8^����e�\P7Ww�o6����5�ߑ�@xG�V�+�x�#�L����e����OL�iD%�5�����EC�+��:O��+܌t����ӈ��	�W��|N-~�����D����ܾg�����X0@������0��=���=�<�/�#TTx�Dg^K(����|�PQ}����
���yX�a\��X�N
���`���KS��m��uF�Q1�ש��U����^`T�9�Q%4�z��M:�B�x4�5w���9o��P7Ǌxô��?Z�Q��\;*/�۷5���&�F�MU5�t~�.��t��.�	td���%�E$�p�fNT ���꧔�T�Pd~8F$�串y������%}C��:0�=��O��*��c��4�T��<j���3�GG��װ�щgM���ި��NS�㟴�,�� >��K�M"Y��e�_GI�(i�2^G�2�����3���&��3D��i�2	0�[���=�μ�)d���`�M���k�sd
��;H��	ƕ�j���������{U�T�c�J;���&����mE�
@ ���L)f&�*��W��Qplt��N��Eڊ�Rq!����t�p��8��;m�\6�m<Wn܁�P����!F���� �Z��}Q���Ct����5��u#�ҋ�K��xQ�l��ӑd�	�����h��`�,�|�
T��|�1�m��&3:4맔D��L�C''c��gƂ���L�D�]v��W�d�`�U璞�ρ���tVu>�f��NbNJ�m��~e��Yۥ������_2��b%�.�a�Ҥ�%K���긾{�Y1"�6��`�aºl�
��jdH��2Ϫq�):'��̢�p25�#>�97�H��q̄ �QǷ�}{s�����U�M�$̧=;�1{�9��|���!�`.07���β*|,�    *���y�I�2^�D�h�v���AGD>o��3F�ϰ^���7kT�*8^�|Qm�2N���:WC����.�h}�ve�pX�z"�'��tD����� ���n�7K�5�F}��*����Ț���C��`I����dF�g���rYN������m���޾Υ=]�c^�'T�-��b�,U�����!�B���u���7#�Ш�5h~�Xp_�/���r��ZW�(v��r�ydc)ӌ�j�v�}�o�T�	�N���E^�fj$Tw<�YH�S��0+fRձ����o�i�l��:Mq��g<�rE���)9�
k��X�s��������æ5��X*ycǟ�&ٕC� ~i�,��2U
��s�ɽ,<n��GK�`T���U�#"��u�>q��&��fDCS���n�Q�N��	���W���4���F����a0��@�"ԁ`Twb� ��kf�|�拱���4���~�����<\^\�w@�ϴ���������Ȱ��B�u+>D4��~�f�׫���v���N2�[*�$���+��
FMCi1qʥ�s����~S��
��Va��"/߃e�pi�����U<F���yDT/�6%��Jhŀ��%�l3G�U�	-�)������8A�����ln������o	�uOT��椲����F)K��#�e�z%��NT�.&U������Z�d���8��:!���)��ݏJ����_9�L�f�cn������`�n�@�n>`�~�4���T�+�֥ɐ�/ޣ&85�����G�FNj��*%8U�@B��Tj;��E,^�	*=51�S�p�ʊYmD��뉶�&3�9�{�Y�9 �T�"��Ʊ؎��?��V��Vk3��|��O�H�;|F���������u^�B��	�cQ�pν��6���'b�i���5�L�Y	��a{���!#��JU�r�Qq����?��742U@�%��M�>���լ_k�����Q����ot��=o�d��r}��I0:��[����W��|����q����Q�,�	�c�&�@3�3j�� j���={�^��j�c���&duh�N�#����$szZiR/#��!!�R���쌑%�7LU��c�4���������Wj���4Å����,!��ј���.��g��k:�?s��V3�ڤhNHz�D���+����,;��|�'��z*�ϙ��
'�2�"="����E�#���؝R.�Y���sDUTͷa�^�]ȣ�~�)�2r���X�O!�4歭�`ޥ��c�
�26cw�^�w�,��~a��m�<	g�:4�y���p7�v ��j��l����xm��*�c�_��"ub���^3~��o0��$���,���Q�D�(ᭊ)�"��f�LV��T�}��f@,����zv3����@���x�6
��Ѫv��>���?�Χ�_�;�^���s��苶��0,:ʋ�BEq�5�������:�U���0�$� �N;_�����ru����wm�[����q�RN�Az/迉�<X^nᗷW�D_]�CT���_�n�(�f:o;�Um_�utO�FU��8 KaK���-�жp�3��i�U�K�Q��`�MF~A2�w|l�Ϸ��W��\�T���5���Ba�qno�S�iN��07+����9OA��]φ1T�H�eݍX��J�.-))����Џ��R�J+B�G^�\�g��~Rz�hiJ+L�v��ho�h����о!,�W+eS��3L�6	@H�u�0ޡ��(pM��Pض�q�i��`���CM����{#����&��wF�"��.��`��kDh1�	=猈���	�[�j�ݬ�a�e%���^V���PU���X⥍�U� UuqRU���\3�y��f�@Gh���l��+p�4�Ֆ�U�"��J��Pi�N�pۿ��5�Q
�V`ɷD��M��(褪UKe��f�"�Y޷k�·�Y�|�Ύ�����?�++q~D+㟲��7=����\ն��+ 7�W��SY�Y`-G����}}w�>,�}��݆K�j]SQ�s�ъjD�f�{�J̧�]�_o�p#�P�$L�K��V��3Ƕ��_#������.R���2]�aܲv&��}t|�\�'7<:�w����</,գ��+�[4:S�C��R��Q�'��#KM�	��܈g���G���C]Po��)90�q2M�N�-�E+Y�����C �?�0H-�I�:��X�x5�ED@��aT`�H킅�C`3_A�4�4����%�����ӢV�zi̬��gwUgfNg�FN����Ӽ�v���$�K�
DD7�}b!A?�����o�=о�z�~�r����7��7�Z�.'�|����x���5������d���s�r\�*4X �ғ	X0tD�R��Ȥf��)�k	��]N#��R�*3>��)<��ij���7�*��t_�P�L�����o�v�����<�.{��$�!�ޔ�נ��u�O�?�����#�s�y�'����M�6��dHpX,)�Y1��a횷bP0�U�҇�Y\q�3]�d8~@x*�� XVz3��H��O�k�S_qEB��������Jz��%�5����X`)'T#�9�	\�hV��#4���t��� �>�lo����P[��0�X�p&�d��v��-@糛�ג1=��W�L����*�2��|l�X� <�[��Xq-pR�����K"����� h~J�-�cM�@���/���P|��O�F�<�'�B�'D���+�c�@��Q�6(�0\�7)*-��'@iH�T�O��NO��	����~B/Lz��z��!"��â��EW���V��K؅KO�o)|��\l/ g�����EDk�^o��}]q�S",�����gB%� ��Sv�e�C�Jr�ηl�+Sƅ��q��g��A�Vp���e�:���.?A�-����8\���#(����M"M>j�5�mS&�
���e9H�N 1!/�PcR�qk�,����:+�(�Ѣp�\7��Ç!
���m=��Ȣ�D�ۇ\d ��rHl~�7��.�������v���R^P��Y	)��!mѷ�!*�M��'���v�oQ�OUu�Y��>L��4MN�-���M�V#Ua�bחeZ+>�=���S<,��qd�G"�*�s��
M��I+e4��{�ԩ�(7$��ʇ�fU��ֿ���򗒪���ޑ�`<����}j�KIu>� ��ל3��C�Q3�AJ�@gy�c�;0|EJ�b0ǈ5%��le�V+7�T��zE+]h,>�LY��h%oBR�D����đN��P�O�B<�{8�G���8/7�tW�uPͣ9�J��x�̉�B88z�5�\	�j�������l����`���y������+z�uI8@�gun�K�A���V8�Tf8D�K�Z�	g��/�2�e_�ڇ��J,�[Q�)V�u��}�i�^#��B����(6�����a��y{�|X����������mJ�Q���.�i���W�Y����!���,�������N������������qK�	�M��5�x�߫��;�hl��z�	72�<��>�H��6V�{:�f�^��֫l7�����!���� =L�nk��E�X6 y��Q1���W��U��+��5������w�1�Ġ�zHnk*�qr�c��sy��p?\��ǍRY���
'������..A�t��RB���>r����wۛ��m���az���ݔS� ](��tIa8;񋿼^~�ZS��c� ���9���	�/����y���B�	��dV��,zJ
\�x�����y���yG���*�և5p��T�¢X��Y4ҫ�H����G�`�r)�q�Q����f/@��^
�2���+�'�B"�.N�����z�d2*n�	��8ս��p��}ׇ��*Xdh�Oo�i3�)�b�u��PX��%��L_�q��U��;���L��%&���(�fl�{/�I��R�����z�/)�E�-������\�:��r9�Pخʜ�[L���a�    ���j�
��1��R�U�C��F��%4԰ovu�"�T� ��Z�{'[=R��������P�u@t�&�~1x�����R@�z�&�l1K��6AOc?��qFUiM���RiZA���C[4ʬ�>�<Ź&�ˑp����)�?��?��F��ltu��IGQ+� �tT��0��H^�
jN-��/iLR��Uř�5fnZ���*W΢m$�]��]4V �HUa�=V���i�!Z�+J+�)��Y`��}즕�Q�����1�^�\�r㋗�o7���2=���0rH,i���ų���.�$j�?k���)�Z������eg�$�
�{#Ѱ�l�-��o��  ���^^қY��+0 HQ�zl��5`�B�I*�q:N��@��S�|6 )�Va�������C2Y�)��t����i�hO���C��f�T�a���bh���Y?�Fey��8��$>�3b|�X�3��D@�0L{�3bb�X
�Fu���0���42�6w����������I�[3k���v��z�[��]���a�	W�@<X4�+j`Ђ/6oֻ�&���� ��^����˕V��4p(W�7:�lx�����b��{������]x�/^�oo�n���������.���j6{5�ju�X����z��������لN�a�xu�v{��ܿ�B�f}E��P ���ن&��kx�7[8��MM@S>�`8Q�5��o�ay,4�4��d�UcT�^p�����zƖπ����^5��r�o�K�����z��|Z�P�ǫ�B��꫺�moC�m5z�����M>κg<��q�}���'/)"
?0��.�m/���k�����]uJ�Q�3�2�M�]�������.H�/�wA����Z��o�u���R�R`aT��fL`��Y>� X�+�G��o�o7��"�`�0sp�L�k=��3�AX��������ց��! t �`��ZԀG���O�3�
����@�7p�;�DqK�k���N��K��չ?W>/�JZ��*�����m�ʨ��)��,w �ms�>?V�f���"������/��z啓���U��(�o�"�3��L�Z2<���mt�A���H��^�̭,0����C�X�?�n���l/��:nn�?X~�xs��⏖���h){�ؕ�8�/�Hc\�?���z�Ξ�*f0���$Wf.Uq/T�PU�BU��ߟJ��Y���n����� �@<�6�?�c������(�_�W����b���	�}���DU�Rݧ4�b�/��_�ɿԓi&��N�e��~�g�e,cP��a��v�dr��/L8J.̪UJJ�y/F��<�on2�-\ƓeIA^���|��u�(T�I %���`�x�DMPd1l�I���0`��Q%���>��c1�E�V�O�(�a&ׂ i �d��g���%)->�v�6�-�6rlT��0�G*eeW�m���↨p�ǕYq�EvT��t}X��#�����ޕ��q$��үh�P��\+�ʶ R�a �3ř2{��=$g�#2��Ϊꮫ�Z��və�2+322��L^ek�8lw���	���+x|�ˤ��R��@%߁~	�Aq�b���}��w�H|�6�Dx�M:��+��V��q�<�j���$ic����r��<�����<����q���1,8=Յ���]��vR�M��A(�o�t@��Ƿ�(�Ȑ7�7ۏ����0�ʐ�M���AyT�T[MU�5`Ç,P�X�����,g�qBvjT)�V6$g^���Ů ��T��x4P:�o��VۚGwn>�T�%�~������ ���c�f��SCu�b�^�?�����[o���G�
E�.K��/���
n����g����$�R�P�
�r�>A)Kֺ�3z�Yj��Հ���6+�T+�]U�	콮O�ӥD�H*)�$��&�x��iP"�I��6����?췛*�N��E*�N�j�X�%��1��-<�@���`�߷jj
��@¦�� ���8�����'�q�0��q����������[�mo�fE�EQ(��B�]�@&��}ȑ׮��t�Um8!�1�*5�H^����n�H����Z0�&F��)����v�6 ���*���ڞ.(M�P�DS?? �����tB�J�"SJ-%������g��-��nC	5�)�|6�ݢT�'��hژ�l�u6�.��*W�PS�ý�1��]8-�U��Re�j���3+i�B��q�����y�j̈́JS�;�ٿ�yjd��)^q9o
�Ghѧ�s�j�l'���E��6M@.j���3-��H�\X�x������5�G�)�O�l����X[V���K\�hȏ���j��
W�����	�r��?I��`�m���Mį�T	#�c�h)�
e�&g������1[�F_�����n����?e�(ad��Y)�X���%�So�03���\]x||b2����v%���~���;�� h{�\y6�@���)��vC���Â���N��u�����`R��x�|ɠ����18<^Jo�?YC�q��L#�Z1_H	dA���quD�u�[���ϵ�6J���N�g�0ESs��v�dsO�ϲ۞zy3�9�o�~�/����.��.&�87ӮnXZ�a=�z�}�l���̸�f�s[q����	�s-�S�Ph�<�������͡5�n��ݔ �HA�	|2���]�?�b���@�8�}�E�*�0��V1�����ƚ-R��Qo<���� �����v�Y�-��+�6 �?�W����"ʚi\]-m_���u�.t���LRS���s��ѓ��}����>�x��!��&��\?iҹ�~�1Od�:b��T�
+Y�:uJw�{���n4��ΐ.�π��xc(zZ5�Ğ٘�M�UTl�%P����s��c;���{P�JW�"��kx�-W��0$Ӏ�Ϗ77�&;n�dP��[�] ��p�Q����¸e������v	�ԧRa��,x`�}�ow7[㹒������l�z�\�]F/��������>�I�$����/��vEqu��X�����19��y�/V�c�?�f��_�a�t���G7DMd�ͷ8��n��-BTAB5�1$�-1~@�ٮOAh�WXa0����Sw�)k�p�F�03��P����7���X'�X&��hBl���?ח&�in�����n>wߞ�[9��A�zrec�a⑋���rG��#�'9�I��u�1�	G�+�5RLk�F٩%�b��Q7v���;z�9ؠ�k�s$�,j�6n�=Ʉ는+�@�R���BQ�({�ow�q�9р}66SIb;�.8f�u�b��.��)�!�U�Ș(�/��?�p@O�)�,\R'��R���H������ɬ�*�z��SZfZ|���x�\[i�+]�A�ߢ�r�V��-]��qI~vώeR�1X'�(8�[v,r�T�
hYg��4�*Ӹ9f�c��
i�,�=�����)p�������b�o�Z*cE�`�/(sTTd���c�:f�V]!T�(�����1��W(�QP�0&��E���hf�UӖv�z�Pd����*>s�]�Y�V��z5�u|t2JL�q�%�In��/6��O�@���v�*�%��"�}����]��(���R���F��1s��J��~���6�'1��(-�e.�6ǰ�%k�y����"����l	���]��~{�%>֢a�n�6�>oؿ�}��ٴh�5���RU�c`��vݿ3<>&�8T)�P�J
ߴԸr��)��� ���6��x|F�bR�۲���c¶2EfH����98�ԍ#>3D��2�qj �=Q"+��e�-��D��ڵYFz�eM����`��l^|D��>w �(c�?" _]���1nk�SbA��
�HM��Z�<ڼ�BƘ��R��(1�%�O�{m�w��w]d���m�q��e"(?֙�: �� ����h`�d�s��QJ��A��\�� %���A��_4j{�a��4Q}<��    ��8�<���_�]�%j��s޲U��E׻	#'G�R�P][Df$��4B�ue�8���-�����Z���{�j�n��[�y�};��;�H{v�w�ú��/�����W����_(h�ge���bJ�d�UG�ؕ��]��2HIb4�ϯoN�Uג��m�QJI��X�0�
YJ] �L$2ӌ+���"ǘ!�<�A����m�YLFާ���(O�
��PT�p�n���+"xJP.����bP�b}��[IJ
X㙸�V��-���Q!�W��*}�}����OM�3)U{QX2PQn���qj9D|�b��gc�nW����:�z,�� s����/4���]�ۂ�nR��:���b�d�'ۯ.�n/�6^��h�@@�W9���l������X���\`���6��&?�ñ����6��|���=���v�`~�8;f��c����`�P����c��N�-b��c~D]�s�	g��̾�?}�_��d�Y"�^&/w�u�z��؜����_׫����e��2���rKhq7��/�ZP:���C�h�����ST����5�[Z���5X]���;���b�Ę�I	ì��5@XR���O����T�[�[O�.!#�M�G�e:)R�L�����Q�����j�>L�p@�L%��`����K�:~1��`�zI��IW��	�����4VQ�Rj[4~�����;�|�H.�����9c�ςl�Ms��xv���Q<�D93�~���L��������~�Ȟ`���ȩ�!]��*n����f�vp���Mv�E��Xi��s,q��))������!���e.f����bY��ݵ��g܊�1#�d�EL����>���W�ł+�����*�~.����̛��L@,/�����a�.F3����������80��,e�bd :y۩(P���4Qr[�w�����qUB�i�^��yYS#�G�236~�l�$�g�1��r�N�����#��C?~�)����L��,|�S��2����j��}X#��Kۏ�q}��?J6�°2dX��<�2O��Ӭo���gQ�X�BELzNqq9m:|z��>�>�%x�5ִ#~>���c�+pL���KQsq���Ol^�3��[�;bb�.�X�S[N��"�e�{�ĶRlt�����"��a;]l{��N�aD�G��o��~{��r�6IA�쮈r��	�Z\=SŖJ� 4��,;fX���D��B��s���h�:�,����s/�^�nY�bu/���)n��S�5��_�������25���
�1��\�K>�k&��ܞ#g�t�=㦛��Y+`�̽�S�sQ�+�&[ �a�E��rےH%��i�k�}��o�ԓ�+��`3%�ZMt�{f����ٙ��L�	��{f�k�t��tFp��3�|�.���9��+�FyQR�ihq�����	�/Yʱ��ů��s���ַ��n���jH{V�2����P���݋OYJ#���È	�On=��b�ZVUJq鏺�T�؄�]�D�>���g4��C��_.����z~Yj=�������u8E=�8IM���1]1�7�,�S[ж���咠��%w��
M��O�K9q3��/���r�Vw�GN'�-��-�Sa[��b�ј7�d���S�"��9���hcs�4� �BY<�=����0_�~��0�_GL�	#�ޗ���Y�/`����.a���>bF�*Xx��dp��c��ȗ���ڶ=ڗ]�Cr��B���I!B7��޲8��"Gʦ�+��a��F�{�\�=s&�W�f��?�ҏTf�N.�+�����?���1K�cl��ž4wU����ɗ����-6�X��^�{~1�^����M5�_Y��Ш��������|�����=RQ�T�T���),�iDSr"n92��������_�~I�3���ǂ�>wS���y�2��_�w]Q���x�[�+�y]�ӢM�����Ң��@)�XYb�2t
h�^��ls��3u�T}퉇$q+_ .t�,�c�fXϺv�٨���u��@���Z��)('���i)��~��+X�@��+�1�Y�TiC�&����Y�Bp{���
��0�����kO �M0�h��g�W���y��ysu$�ZR��"%}���HI_��1R��y�wnb�@c�V�(�G�؞M]�-��z��������K㦾
o��g�O�Vu5j�qs_�W�^��j��LdT4�&�0����8Kmp����WXet��L:����p�g�Aϖ"4r����p����7������F߼5G�����hEcK5X��!UU�V&*h|�ӴI���h�a���2=��q*s����2%���Y���3)�*Ċ�6�s�L1S���S�m��^��|�\���s���W�40��J�TM�b�h��g��W��(��qU�o+jc��D�5W�D�@"y�\c$&\d+��'þ�xW�E�b���\��q��4���Z�������r�=���pIvfp}0�Y��i�.�f��0�o�g/?ϙu�[��C�e�=^TōU�{\�T��eR,P i�Qh*<s��_~l��_�M��r��蹸��]q� ���q_ܼX��]��G� ~|������ǆ��x�%�������c�|�c#�ٸ�Ï���p��伾���&ޘ;a:�H���w�D���Ya/����&�������Ю��S�r̷�v�~�-`=�1��9rb��}#���옡ı`4=#��U쿂»��[����#��!*:t(�pDZ^��SPE�J]=j�����յ,�#LMG�4�-D\�j��"e�GD���)OU�G�6f�U?e����o�K�qqqO�ycaW��l0NU�X9.��qB�Si]S�z��ƕﮈ^�e65�Q���Բ��2Aۣ@�D��0��Dܤ���:hu�<�ᱻMą8���N5���`���۔�3�u
���s{��6�ljW�����m�8 �x�Eǿ��j��j��j�r$�If��)B��h��K���.�����A�9�GF\$Ѳ�Ƹ�����W�l���C����C�a��s8������˸2.q�±Mp�'w�zx�W��������l �"�{z6�b�)�DA�EQ�U2�Ur��2:.zj�OY����� ��I�F`,5�Y���$�,c����� pe<Uʈ����~P1h��o?d�7����n�����hø��w2���rh4B��@tD��Z\�h���8�:�^w=�4��1�SDb���@��Xd�t�"����J����}_+#	:h��E��7>�@�1+�K}�"+��*G��v�}�>�w �8$#��AkAc1=!��`�a$�ׄ���9	T�ʤ�I��!��^����C
o@�&�d����O�w:;ŖX����m�52���ʾ�W� Q���+��%�]���3���X�,��)���b`��G�g�H���������!�����N���j�sԷ���c� ��*2�Z��s"��w�mv[�����K�EZMо�*��!��kA$��������Lhz~|��s��1���~x�+n��"��8��> �ٖ8��e��Lw�4�_-Wf�C8�,���O������̥���;��}eg?%E����4w�%�7k���/�#�3��k�Xf��=#X'H5k�]b���k(�&�K�ZW���6_��	n4���
��]��Z��a8���'��b���4�ɻ<����m��e^toz������<�(��2�<���C�y���1�t&�!�q������v���bsx��	bc��H�/w^���c�^�á×���oΊ��`���8b]$��{��o�^WM+���bh���JL�C:u��O��מ
��+J9��~r)�P� }<4Z8�ė'	���Snd١��C��39PQ�
�w�l�����9L�|�3��+��(��ЇO��um��$w�A'�j�M� �� �  ��� yH�FV5�#��A~�|}�jhi�g����j6y��l�؆D�R���v����B�BW�������5�����kB"(�n���g�˖�üh�фƟ�й@�aZ/=K�I�	�G�=A��&x��ٗx4 �s�<ǜ�.b(���scm)�ΓW�}Vl�}��7i����cJנQ[*�`��M��}�ҵ�#��#�ע⵸g��6�Z���UvFwX\D|7A\�`8Q"PtIn�u�ԗ�U�L��vr�򩰆����=���(@9S�� _[x���[JA��P��
�4^��|��s��O�ǈ�'Th�-#��ߏ��%�AM��͍;�>���d>&�S��`��D�ķ�#��Vb:���}���R�8�����	�^��T�P�^�ndW��k�bd��/�Pu]�W\S���
��L']�w�������g�k-*&;���v�_{e��L��0�����{QB&������4#�8Ѓu*�1�{�$��k������J`�>��������o-�
�\%�}^���t�(�b���7�ޘ��A�F#�R��\�>ن��N�V�^��O�8��0�up:�[?nn�j�����@ [���%}�ϋ֧���V�?�W_}��k�      �	   �  x�eU�r�0<�|?��H��^]I.��*9�A�U%�-��3z�p.��==j=F��E�YZ+��~u�#�����"��
a������%�-Z9�\�>���m	�+�y��9�X�D����0�kE���q��� ����I/����O�U����u/��ߥ6Q��\�NS	t�n�zLc���\ܭ�ߥ��=ĺ��gh�j�6E�2'�\�:�������WC���!�������T.j6������r�kL�2֭�GZ��51�#�E.1�Z���_1$��u ީe���d�adt��Q�";�	tF�.`��eE���\�|f1F^��=�A�,�UF�a��J�)�@��!�#o��tA ��9M3�2?�3�O!D~9M�?9���K��$��{r����� �E�jqΙ��a0�k��I�4] ��}�|����o��s����16M�y%U�YRee���|�MOZ�*�i�/��mN�+��p^IN�9g�q�������mr�;��ѫ}�g�1v5Œ�$��}�~�&ϴ=�-�o���h�/ �����7�]��FU��-���%����1�;�K��k>���&<}�?��	l�3�i�ӳ�3&=ͼ'2�������a����Eo�XN�Lx�G����\=C樏����药��#�c�ޤ�����P�>�����Rs|<����"����      �	      x��}[o�G����W������]V����$��ז)��̶$��=�%�݃]4k��t�j� ��qN\cH�]]ɱ�ȑcV�B�������_~~���g��ݛW����\y���/�W�/�??֛7�����W/������������oo�����{���_//N���B?��[�����|�Ͼ������9��g�����1���<{�??]ѿ߼���ry����y�=9?�������������O������/gO�|��a��O.���#�	OTw��g����J�9F���9���g��K�nu���W7'������EO^��?��z�����k����?��_O_\�����m��'J?�>���u��t)�nE����Yyh`'%�H�}�����������/��<v{{y���gOq�/N���K��Ӌ�_/o.����_Oo���n��?R|��	�.@d�m�Z�u�В������[��ڎ��W��_��yӓ۟?]�<�~K��o�//^}0A���ًӛ��w������L?v�p�Ű>��(�iJ+�K�4u����^C���َ;�ty�蔟<y�ҝ���������_~����Ogoo���	����W9�'>�!��v[��T�Jm��8����Z�t�������7�s]9�G�xg;|�9)��C{}z�u�S~�^����gzz������g'|��?�\_�����z�߯�O\z��.� K�8���L�7OeD	%�:��F�ѣ՝�vK�D�.�H��-p�å�i:7{��<��R)U{����}����������..M�o�]�\?�pu���\��å��ӟ���
u�������VVM�}v�c��B��"�7��C�z��!��nO�_���k]���͇���W�M��\�]<���}�s���;��'�&骜�f������Gt�A[j�A[�$I���{K4��5�ݺ����Me�f*+7F�QD�����%S(G��G����?�4����뫧���ry���v���݇�[h��ן��d�V�� �VS�7�>�����e@y���A���rh-��1������kYf$�;��k(��,Q�kT$W��	bJ ��./��UUd��it��a>�"�v\���n�N�[���N�r\�H�����G��ze�#� }�k��w��䂩�8ڑ#�Ir����O=6���La��;0]�|�>������/tz��No�|��G�Ş���٧�������ݭwb����l��6���/ >�G`k�i��Cw�w���>�҄ѿm�����˛g�����ŉ��^�uPW�'/N>�<�h0��u>�nS�&~&\p*4C3�]�3����×�ϫ�+@�W7�� Oۗ����Շӧϰ>�M���0~	�gr�sqv�HG��뀧�9�<�ׄ�y�L��WIyi�  �������w	>�\�Q��}��'�|z� �/ru~�������G0�/����������z��_��Vr?�%��w��L ,�?R������k�>���Xu6�	�bǉD�D�	��9%����iu��%��av2�-d�>J�b9�I0��YF�FO�q�G~��=�@|���Q�F��
3QH8��rLs>�6Y�֥;R'�h}kP�#@����ʡ0�ڴ���-w_��ds5<Q�K�k�{�%�Շ,4�VW2�x$�_P�����%.��� �u��E6��:$��>S�σB��=b���Ch:]2-}3��rR�օ���JM�����u����������d6I�;�Y�,K��dXꜭ�n�� �n�x�F�-�Ի���M���4}�S(*q�{�g���3��t爕��y�/I���J!��| zཿT��z6�od��XJ(1��p��<!�c��2B����7�$�+Y�'���d���SsO`V��=�q���6��U�p��Sp�|q¹`w�azGA���J5>N�L����qb<ܭ��<'P�K�����s��l4?����n�#ޢ'��v�;vUsg<)��!����2��%��ޭ�ۭ��m�§����;N��-"зQ>�9������V0��8�3�J͞�����`_F�VN������;��d>v�k候�Г�4��Ѧ�@�5C��s�97����8���������b�}�2�a�(��Ro����X���ځfM���h@ ��� ��q�ٳ�-0?F�	D��+���҃r��b`ܶ}�o��� �� C@���� �@��ݛ7!�bN��vR.q&���HZ���C�)�4��_�[�\�]�F�l]`���@Z�yc�@�>�I�.�u��7ʅ[�����`�Ҥa�$���Xkrŋ�O�������ɽenE ����� 	̽����8j.@��@��r��2 ���Q씡mj�[�)\g�'J�r�ٛF2$v�J�m�A%k����=1�}rC�,���H")�{�2Gk QՑ��+��r��S3ꔇ\W����{,�Z��AǍ��, t�<B;9(���@	��,�t�9����;͚g̜�sz^y'P���$*�̵f����U���Z!�D���R�� �Z�%4���5�&"�@�@�K	~�����ha5�;�~��fz�2�֐�Sq��4�"M�?��~?/�s9�f�Y'��C}Mx���f窩���P���.J�i�}�9K�1 ��:R�@�Y5��s<r떟P����_�e�6R\����lhf��!U-r�i��-$f���N�d�Y��+w��[n4��Qg����E���V�,Ko��>��r� ɮk�@�O�^�Jk0��hI~
�#��Z,���0��c��I��6�J+��/$�yG�$A���.�tm.��̶2��=��6tHѾ�;c������F��Quf�rve:p��v��,��xK�v�Lk]`(�՜���S�=��"��*����K$$�LpثiMT��0��G&�3����r�Sz��.F'a�FQ��F�h�m�T���a����o�"0��(A�/�n�v_���e@�F1�^ڤV����}� ں*���҄"(�J�Ï)1�\k�A���2$����a8���m��q�AZ�+�w�G��5�ʴ�n]d	S��d�89�gN��IP*�xU�|�=?�=ںxg:};��i�Zp���>�b�	kN�.�;���Un��)���ר��1R�\����\�%5JK�� fq:,��:�%,u�$CCy ÷u�ie�`^z�f�s���Ӭ 3W�=�F�n��`�bK��=��/�
�DK�3�
k7`S4��'_0#`*n��9`�����r��^� �N�ֺ��-4T{Ú���I�z ��`U�X�Y)\V�Q�9�cI�k��@��Z���ݒ��5<�4A���9�L��Y���!�A���î+X��ZC�4����$t�����j,c>�s�����ZW��<{5�iT�J�Qyz��A�w�a�� !�M����9(�K�2�k��~X���� �6L�žR�-M�ؠ �4n%I���/oR�^t9�Fh��@\���6&����[f�l]b!.(���PbqdE5!����t ^�S�xUY8nA�1՛Aj�!aÇB
[�璜;�[��Vͬ77dlҒUt��p��QPOɥ�;�[�ו���/�#Y�%,�o��6*���p���;�|�[e�j�=s�k�̧\g�p(u'�a]L;�I6�\7�U'`�+��=hju���iU��wV���*��ρv�iP�;��V^�
��h(U�9��7;��i�Ys�X+�t]i�b��{�5{�v��H�w�T�h9l���K"�e��P�A��U��<��^Z~���������Z�%��*

�@�`�[�:���RX!Owh�DH�w��X=��.'��� ۺ����8� :��*$�Ym��lV��=���A�oΜ��J-]*�?[��EJʎ"Y�ۺ�΁$�-Q�.o�xt���{�r��,��ؐ�}t�On���-6K��Ҽ�ut`���+~8<a1�{J�`�����	�A��;���q]ʚ�&����	4-A��� �    �ήpo��(Z��x���(UK�Z��:y��V��`Ϳ���ϥVe�Z}� �;ߕك�ZT@p�cSǽ�Nr���{����8Yp���.ǔ}ڂ��+S�$F��T�YTJ���!�{�"���BУJ���'�c���5�J��1`�c��,�#j��nuU�)���7��Fgh��h�Oo�0��~�[0U�T��U'��Z����XFM�T��Q(��4��Us�,8���)��o�haN7k#��e��`��;n ��ұ���t�tX�ȯ�r�4��Z87�ܫL���������U��w����S�'�V�հq�3������j�� !�iK�
F������$
VDK�B�A��<�0���Bʏ�p�N�⪟ckb��:�r�d����_L@�S��#7�����݊��!��P�I*xU��4����i�+*��H-��Y�n}Z��
2�R/��}OY�h#c�qH="Y��=RIw�`��-Q9nu�> ���̧�\����Ӿi&bH̭����ⶲ=�:�ƥLK��Jp�����S�+�T�)R�%��|�Bq^eXZ�ɒ&N�Oޣc{]~�p2N�,����sf�Kf��<XlkB�Ә缲�壭��a5��E�B��; c���X�5}��@V��y,o�;���nͪ�:v\z�.(5Vf�j"3l����_�՟O�%�����~��O���������=���Ɵ�o���o�����N�O����x��o�y<�>{������7���ק�'|y���W7o����8���������-J�E�}:��}�ܚ(��\�t1����A|}}@in�X2�w ��s��gs�4���?������VF^ZG��Y��!�ܤ�� ,A׸ɾ�\���t�G��t%�Ń������-eP�麷��9s/��6R�f\_ҟH�֭8��o�&����v'�.��}䔚��{x�uM+`�.I�[O˾O��[�޳�pts*�������^ɮ��CŹ�f�6Kn؄ &�Dx��'<���w���w� \[ӂ.%).x����[%�a��)�3rܲ�}v��X����������q��֙�bX�k�+>���oM�%XK _��m������T�ȚkA�s���	��g�b�o�:Ke-Ձ�d`��et�R�J?��{����k�
j�^��d��.T�ץ�� 8`ȣ���*D^ч,�m�����"\޳��,x����3�GXk�ͫ�Y��6�e��8���U�Ow�S�j�Z���q=���m�����ʛc��s�� K�f(�B��j��I���^�u���ޯHs��r2	j�
�,��Lxg�Ī�za�qp��u�XE�����Tqn��
�[S��zi�%�=N��wұ�v��Jֆt0��!O*ʭ����4Y�G��?ҷ�V4ӭ��zA9��\O�����xi1��t�s>n��{k�%����[7P�Ly�R��t�W@�\��`őq�9�k�����XkX�!mpί�\g0*���%���_N�ª�zr�i�l�Xr QV	�@"Ƣ uy���sw|W�(n�@Rnk;z�X�Js1S�b�L��>�>��n-Ț��im�ͲLQSJ��F�j�
=�}��<��gǠ͠;���a������pL�6�Z`�%�Y�Ywf�o�M�-��"ʜd�7 �B%�,g������q	�S٤��<Xw$�;��6�қv��c)�����KEk���*�Z���F��DxU��-��}�b�Α@����Z�I��uk��- i��g[@-�p��a���TL@h`͖��Na{��H�]*i�VD˒D�2U�f�O^[�e]%�~�d;�M�y確���B��Kc�����N�Qd*)���>�z�z� �b]h8[A�5���*^F(�XQ�-J�nvڬ����Dxa�[A�F�.�b����j-;�H2i�K2k�%�`)�@�u��NB���T�z�XTٻ���/a���r�o�:Z�����
��$���ԁ��2�86߃`Y�lMe��fNne-���&j`�a� �-�L\�,��N�A�<����8���.In���0v[��"ӑ0K�?�]����$#X
�t��χ�A6�`o\�������ȵ�m]A�6S ;Y���;Ҩ#��g����;$�X��BV@e^�ɠ ��N�i�	B��q���o���V��4�y&eH}�<]��֘���~��&߯�wdy�[�n7Ō]��
`�PR�7��ۧ?hGҿ���r�-|c�9ht�1Q����Ifi��ڃ�����e�l�V��*��i݂� ju���>�=b]�F�|ْKC萬�gM���㠓g�}�w��ޯ�۷ꎉ��N�x\�C�4�O!G����8�E�?�W�h�gO_���k:=��=�x�������'Oۗ�뗰/?�^�uߟƚ�j���.8����7Fl]x<�D��������u8��^�Rm��*�&���V�rj^�4�W�:�#���ͮX�r����r�=���.ױ��y4�Z���9;x\���ǒ��c|��ŵ�4D�?�����^9�m]�*G�l}(�``��?,�C����^�(���~]�|.��+a�Oe 8�9X��s����g�C�k�7vzt�X�e Tx��=l	�5�7��8��t߯+��Y��2�`l1��1�{��>�Z!Y�������]R��R�0�)���U�kS�)�(���ޯ6^8Il2��!����<�T��j��qP�C�c3�?���G�VT�(r]�Μ�.n�g�
���+��˺���o� x֤F\Af�Gϭ�����߯���P���SJO���Ɔ�V|A�s|���W4=m�zhm�%0�譫���}�!f+������@�6WY��� �n>;������,��	���ՙ�����9/�W���֏K�K:��a���	]����4�j��>m#�ݜX�5�)��OV�\حn)�9Wloݲ�6q�aC��lT cZ�ڌl><����o���2$��te{	E����6�<݃V5���]?n`���x�,�e�j�)ז�ڀ�&��֒`Կ
Y�S������c�y���Ö��6]u�
��J��Y-����[ҷ��鉬����e�Oj��� ��$/�B��(���U��6_��.��@{��� {�� WŮ����<[sMv+��ZZ9̦%�uי"�T����`�>���9�5"�+d ��@������Z�x�P�$����ѹ���q=��Bsgz 	*_y�)0�w��24�MJ��3-�� 
�2 ��j w�"�탣9.�BnX���J�0�~_c�E
e3�|5� ^�f�lr�b �"�E��c<Nv���9X����������=R�����W��:�ض'�[�jÇ�D.g��f�K�p0�O�s��>=U� >4��/���{y�p���`�+��%r�iu�#��kv�!{{��}��l#g�gI��:�<,$.���jp`P4j �̇��r��-�s��)��89�=X8 	B�1�kU�lǝ���^_����?_bO'7/?��?]�_B睝���.�A6=}z��{�k#b��i�G�v[SJu�&�~��~�fC��C���g��j�h=�r��7� é�Zz�z�(�P����-⫋gtɗ_�����կ��'���K���)���ы�ru�����2k
�e��$���+��@����4�2��DXVa+Vq~g-�(��ch� Lb�
���ڊ��G�Ǎ��m��>9�K#5X�ZxL����N:"�T6E���ϖ?��]�x���u�|rq��R/o�}�F�b/�Շ��>�>=�puq��`�l4�5������U<.�����b[}*������x���V�]fջa�ۄsa<�}��}�*��ǉ�ݭ8����-m&���AcZ3��n��d`�t�	��Ζ�vK�$,ˍًl�xz�N� r��(L��������W�[wv�̝�x����[����W7�?�ܜ�b�ܾ�jt�o�_�U����u��hî����Xwl�����s�S�#?���r��N���&G�`�^���2FcG��(2�2   volJ}��)$Jh�M��=ij�D��)��6ķ��|l�Ks�w��{�����c����
�I�f<Zl�����c��CH�9ykB�<�i����$���u���iX�Yw�c��r�[B�e؈�*0,(H%x�8�V��:+���e[�._�CC��X&ONqՠ�8?``s:��*���<�|��ڬ1G1Sٓ8��=��6<<1Jnyr1�����!W��F
�=[�8l���Q_0��	C�Ac�뫛77�����94�ӟ	���嗓o����,n��@j�rt�߼{#V��Y�r�QK�@��{�����m����8�n�uk�g�BK�
�}%��Ͼ*����7|�ݦJZ��m.�׭^�5�Θ(�I�R5�K�0Kɮ�=��}��Vı�1�nH$�`�pPB�Ŵ�t7f�V���uk5i��-���!;6���\6B�����-r=tz�����3G��c��6��R�^bI�k�Ԇ�п�:�q�g�_+ʒ�s�`�A-+$�\�M�3��~p�um9�jkG�j�,)�co�4Kn�dm����iͨ_9[f��%ou1�~�V�9{�7�»m�����p���Uv�������Z�� s��3�98�,������hUi���w�mݲn-H8��gЎK� �j��x�m[�j�`*ғ�&���6c���`�����I{�`��з�u��Ĳ����P�w�_����:r�RB���eY����Ow!�.��#tr�6��QP��(��w�;���ѬODAh �Q�L����2�Lg�dhM��W�zoFf��Y�q�2��u�ׁK��+N4N����	�v>��h��uuo�nMn�8o�t@��";��/��#0�Ç�����;,T�Kyb��T0�@s�7v  ��Ҏۼ�������d���`���z=����V%gT�[/-�܂�.��֊��dk')Yy{�q�����tMa?������B�m]�f6,��[Wfq������Xj�l�Nґ�
���~�wB)n]z��3q�2o�����݃�;�m]qMOMk0�֘��6�O4�hS�<ȑHGӷ}����+�B�,Y��Yy�$O�U���&DBBǌ�N~ϗEX3�����d!�**j�.�Q~�}���[i�_,�3�\̫�1l��B�z����e�Y�@����۷�jȲ���柙�w���@j4+�m�����8�G��n��S�nӒ�U�T�� �-����X�<��1w�������e_I�1�eQk��B�k���_����r23[iYd���e?���.�6�U�C�3�iM�k���ƺ����F2��`3{� �X��u]vXl	[�-�w��XØ��o�f�`}"�n:����ۼ���_���KŻ	J�)Z���A�k� Z�9O�16I��6.����%,�n�gsr��W��b�� 	��<{���S��Z�p����@R`n�e�X��h�-�A;�D��ś���$^cЭ'��g�{�g-ZA�Z��0����}��ׂ��[Ȇ3TvQ�o�t)��@�i8'eF�&�#'h�}Z��3�t=k4��)�q���#�.��`��RW��m�����ܕ��.���5����SVM�H�5��'P��O�Չ}�B�~6���v^ǃǢ�"��������E�'�����-�Ri	憆��ԏ>�7�<,�����g@�9���ܯ��h��h�S�y��@	$FA��UcR3匭J�Pُ�-�w�5��w.Ǹ�����M�K�u��}j��~���ro�WxI�phP��ƛ�����L!H��?����֠���~m��B��{dk�59Ϳ-�)���3ŉMOܡQ����� �76ඤ�ܲ>d�)x���r�9r讖æ���8�y�)=�n���lK鵁݃
��ێ���I60����ڲr6��(�6���BΪ[i�>'�z��Y=������9i��O��i��$�!��Â����}>���tW&j�]n%�+�=Z�yz-.��ǂ�9���~� �_�%���F	�O ����acv]�^U�K��}]w��>�'��5L���3V/��������F^k��=Ng�����R�a��b�X�(W)�,k�f���RR�|X_1/�t��L��ꋒB��U]��-V{���Qӑ����]�̺U�V	�Gbk���(1�ZB�L�Vzϱ)H�Q�=$���X�k�ڰ��U��A�M�K����V��u`*}f:n����cO����^^��9=�������w��ogO_:�W���ۓ��7ߟq�se:�L!m��̳�tl_���Y[�ַ��f���pѴ\�ni�lԫeP�œX� ��ڋU0�G�o�ݦ�\������n %�m�n�[��Ӱ��R�q� �G�x��,'S`��k���".8�mj���LZX���k]��K[&�<��}�σ�� �]c���m͛	x�Yۺ��a=���6�t�*�A�8 kp�P#�� !����:��J=1udD�Ya�4�����,ڻ�VEb�ݻ��o�a�60b�C�vM�7%	�+(�O�f?���p��	@�57|�K�;��ِ��t�b���B�l�l��*�O���lo\�t��׆3&��=�\��
d;��e7�a��QC6_�d�~�V)szsu��l^ݜ]��.���U;�~��Ρ�������JfR�{메�w=$	�{�m�T���	0NԂ�G���3v{���vgy�O�=}~}+�co��W����W�?9{�V���Vט�O(�y��$����򷀢G�¥��Ok�tTJ��fW*�MV��P��4�YG��kjTA�Sr@1��n6��xT���y��3ߊ��W�F�ڱ�`�g�$��7E| J����=Ƥ~� �[if�r#����ܭ�}TK����8�>c��q�����v�+O���yH�u�uQ�fHY?k�Bӆ������`����|�x��|�͹Y,�'m�����yZ�\`.m�^+�[y%X���|w�6���m$��>s z�h�H�:nu�U��8VoM�0��ֻ����(芓.N��BM����;㭻�u.P�U�e�R&Q��@�K�5��+����<n��Ϙ�*�h���rXN�{��?�> ���v�;T��#ܭ,�$������j|���6ƞu̔f�`����s�g^��
Km����aڼ��9@b�	)܂��s�3�Rr���,��wƇ��kJ[O|Ge� "��U��6��#�R~�������kԞB��V��z#7��Z�u�6I��2,|r\9�_}��-oHUL3�l���!��p[�4K��W�F�R��o *�3�;�ӭ-5N�z���"��)C���~�^����&Q��Iw��oUS�Y>.qn�YÀ�������QY��d_}<�xss��ݯ�o������-X��@Ƴ�����/g�X���n-=�[��j�~7 �v���}�.�<KiS�ݣfC|y�;������[l����������ד�Ȟ�K9��u���K~-�ov��:5�-[����F�\C�Yoh��P�|4�>�}>��ã�����~������v��      �	      x�3�L�H�-�I�K��Efs��qqq �<	�      �	   �  x��VMo�F=K�bn=y0$����E��v�-�@���=��+[�$#I}9r۲�>��<���CE*f�3�B��m$�ʡ�f��u��\A��޶]jV}�/�\$/X��U�3t;�n�خ̥+8��t��H�0�>㺊>��f�Kb����n�3��ϵ��5S0S$@q�Q9i�iC{��ЛnX��4^q��׾�i�#=��X��Cۉ���7��b��$�[:��em�r�1
D� �s��c~�ڈ**+����L��C�oۍ�-��Ӧi6,W��_C��>�a����y۴]��C׮�:u�(ajPc���)��d$ ��Gש�37�/�T��.ب�:-5�~Jw�~���iXm!Mƀ�R��I逧b�*S�HA��B�;����ڔ����ar�ӑV�p��u�p�5stv#��E�U�2]��^�Z�;*H ����ң�֝�]E?�\�|�xv:D�I"�m.�.ѡ[��[UhO����>(�W���_w�T��x�=P���������x����$��bG�j�z�qBT���bM${I1�)���	,���e�]=�F���*�-E.�FҚ`�����=�MZ�����QJ��U�*�(I��AKzE�W��hn��t�׆�/<{(�u%A�R�����݈?���&=�z��M��F��/�f��~����]�5��O��FE�(�
/#�^7
�[����́�g��� Fi�Η�"�
0��-|͙{Yc8'�.����Ֆ�Lȯ�����q	�<�Dl$up@�|���٦y��"��������	ʥ�HDU8;�3�΄���L�.��{�QQU�~�+_&P�Ɔ�o	�(�Gy>�*HhƱ������_�u�_�.�ٿ%o��'^iI
�q�R��q�r��2��<��_z������.��t��m�����?�A|\v<���r���Ȑ����������hP���a��A��V�t������?,7      �	   %  x�-�ɑ!C�&�)��\~�q�d���^{�7|n[w�>t��Veӳ����5��M���� y�jBLFbr6]�95�5��izқ�}J��T��2%�r�����(�˳S�D�?$�6?�W����'�C3w�c	�n���'�B�q���Z���b�<�,��I�aH,ʧ�%u���.-��Bץ�etD�J��)��!z-)��TL\����tro0e�۝�w��f��F6�o�Ĉ<o�P�u?.��1��n ��bQs_Ҳ-PB*<������{���1�wl�      �	   S   x�3�4��4204�54�50V0��21�20�3262�0�50% ��XY�eD�)婩��\Ɣ���W�Q�eB�9���E�\1z\\\ �o9p      �	   �  x����n�F������fO�k��q`5����%F^�^
��Vo�Y�&Er��Я�f9;��R�~����[�od�����e~�?�����N��o�.[����2���n�/HC�K��\�lT���h�%q�	Iܠv�}ݴ���@�j�%�7��/�8��)-L2w��9a�2	t���A}(��tM�������jO<<��K�W=T%��K���Aݜ��7��c���oO�$���i��nWW�Ir�S6YI�z~�;N��I)8O�G���X�I�8˹Iؠn��a�	�@�`,g�:Imn�������F�ԯ� �J�1��R�p)3)ܨ~ģ���~��\P�>S;���n��ڙ��Uh�X^��g��&|�R.�Wj�����u��V)�t�$�ZPi�v��x(���2"��Q��^���m�����ɍ����և�8�8� ��u4�e~{��m�-����)���9S�6���m�؄���.O��9��U�bGw��B�ؒ�L�.۶Bc~Ⱥ>��oq��,��\i�4��9:����?U�!>?_��0xYN'�H��7�<�-~��:���w9T�8մ�J�Lc��|]/$�M˞J�,��`{��cY�v�q)�{��Թ)�$����s����GI���N�k��VX�\Hn�����)��i�INl	��!�P���v���e7Q?d��S7d��'��*
���J5�>4m���:yb�$	�e\�j�,7~>ܗ��D��D����6��J�@��VF�1&*c���0��`/�kIĘ��k���ο��7!;��B�w�,@��8#b�AG��d
�s�CYZ"�L�.�DN� ��8u�S���)Ά�O��o* �D���ф8����=�:x���П�� P�
�na��P��]4P���c��*~�>�ۺ��e�1�/:F)�l���u�7�,v%
&r�oMV���7�2��5�:�i�9�4W�!��勿���J�L;'�ȅaR	����p����Ŏ?��2| *�3���zc-�Z��r����9<W!^��%(��^�H���>�W�7���p��Up16k�$rMU�L]������|iтx*�-�-�̵ �����!_����׎��m�`%�����"㢐6^����7��P���}���onn�-"��      �	   w   x���;
1Dk����H����iRo��-�|�����y���#c�h	d�'��L��IS6p]d�����)�odB"5�)*D�Nz{�������RyH�'�l���Zb�_
n'�      �	   H  x����j�0���S�j�]�~�m	�PZH��G�Jm��~e�����N�cvvq�(�˅�Ad��傮�AxP���ᠾ���}Ȗ!l�f����14e`rR:�*T��Qt}U}���h�k	d񽭚]��� jZA��j��3�%���ψ�-b[��w[4�!�=X�d�dw�M�T�)���H���^8n
�w����Ү�t˖^�i�p�=Q�
�ϡ�e��쫍e�a3���	SYn�"X�]���{s��N��`�����(�l�U�}:y	G�K���>�mU25D�Ь��qNE]��ጱ??���      �	      x�}��\7��w��`]Ѕ�5�?��A2��c���L ���v����v&~�%u$I�z� ���.$E�v��p��_��_Xu��ڄk���@|�`�j��D�jsm��+���rWV��ׯ^����/
a?h����hmJ���A9ߨ�^����xm�1��&,�ښ8`̀"ֹ�r�DXcĽގ]h���i�ƅ��z3wl�T����R�,��(hU��:�����
/L:`)�k��:y�ԵB���Ԋh�saElB"��>.�8�=n�.Ŏ���ilyZ�S���z�S�:�QW��{�������_�i)ը=�>���<!�
�f�Z{�V�]Z�w�h����[�� ��? ���:�K`����)H�D�p�5�J	��YZ`4���?�5Z#��,�h84 �`����1���&�&)�h02,1�Q�
50�5휥�� ��]�!��� 3�K	��y���j]l��$Ȳ�N��Q�: ϟ�p�Q�\���y���A�e�6�������ß�z�p V@CB��$݁�3P����� \�pt>%���J
�^��}|�v9�nF���P6��zInҎlr�
SQ�P��$$O���+n��{}����)%�}��9�㊧��M�	xs��y'����8���aM�RP���&�,�f�l:O��7IA���h��:���W�s��Cc�ߐ8m��ԵK8y��N4�{m�ѹ�|�"͟�oPi�jj^MK.��j��l�֠��� &�M8��|{���zn�}��Ғۤ=�tܸ���[�=�v�ĸ8a�WB�N*r�,����ժ�,�};K+��'�9TS4�`쀞�롲��o~��2�X;�h=�p�*��ТJ����	���ʢ���t

�PoK�W����HU]�&��^�d9t���#h�z�D�3Gl���`$�qj��w̮�8-�̈��cZ!�r�8��5'&����`����LCA�B&��������;A�j�6�AjPS�va��鱈J�k٧Xm���\
h9��w��x"�TJS=���'�HS,�M�>�2@v��[�rb-M��b���H��aԑ,���'�wo�Z_�<�����Ę{_&�okg���0>B�+���ecZg��}|���}�FlIw=�</ŠgN�A�p��d�`n2��I�%4��pkh��P��d�fM��奕�Y)F]=��TXR���T�Lw��L��P�ԲАB�ԛ��~�9(N��S��N�t}$��s^��"W~��Ϡi�Y=��v��9ۘlaBS��L�y����X5�����i�cFf���p.��~gz��Xbڛw]=1.�H���yA����R�������Wv��)m["C�>�K	��t�T�*��>M�B��ArO��<^<��,>m�T��5;q���F��Ģ����fe��=2#^���%a�(Hp�Ɗ��f�IھD:��VK7 �L������q�p��VK? ���pȡI&�J�B����e��MRB�)�d-��s���<�A��9C�нNֱ����!���<�����0g�R�� �$�Lt�S2�R�++��,�̷S�R*9#��$��7o�:h��=��G����ҭCϟv(f̂�s�\j�OR�����ˇϻ�Z�~(E�ZRP�d��T���~��o�s�B㝦]�h)\2l�3!�͛�;R� Y�)8U���9I�?_�ʄY̒�IA'if�J���)�� �xØ+�2k!��b�f蠝��ЄM�"�I���a� ���`�fT�qI7p���n�U<�	���`�ST̙�E�ş,Q��#���$�R�<��׌ ş��e#4�!���K�ܮ��Z�Fr�h�:��7o��LhGViD&e�	�1)9꙲>)��#��ߠ	{�A�ޥ7S�����1�߸(B)&�m�N]*�z*Iی� ��<c!��:t�Ƥ#͡,�b�i����tt��iFL����n�OOO��>�����ty:��W��4=�J�CV�Y�:��+^�4a�(�W^ �VcRz�b*�'����]4�ԿQ+�	XO�������/G�HlP��>u��RM�L	:�TcR�4c4�ՠ%e<���ژiL�V?��	�?!��/�e׊(9�2���	3C�ck
er,�u�Ä����p0��A�[$�Yhi���.����_����N�����×�������������ӷ�����y����p������V��;�J��S��c\�$v����0�Jn?��6a� thZ%:��ګ:�>�-����m�h\�܂�1�����J
�
�/�&�N�N|����/�X_��%�o��:b�n$[�`_s�
�9�ƒ�*���F�`0ε�{O��
Ks�Va�8)]��j|�qo����P��t���������W#WKF������OH�=U��R��֗�&��v���	ɩ'vQ�:�b�YZ��A�`�;բ1J+���vE����B`������"x��}��^)���a(lhI�� ��J
6^}��������r����r[N��4���zYt�R�')������ϲtNg<�H0R>8K+�_i�H� ~�V��	kdRR�9K	y34�-�H�>��"���5�&�Mƥ��S�R����R�L�ڔI9aS��|Z.�A|�s��O[�i"d����c��,ES���/�ʅ�S�#'��e��m�лSi1�R���yW�K\��ǺU���ޖ�	k�c �cwhr�A�N���^p��[��-�8#D3r��jˬ��Rj8����T�K1s�zs���nϗ�y{w�x�A����ow���ˇ���/�{�Dvb
�B.Ϳw�H�w�����K�V2��R��w���{�|�}8<��������K�����O����Λ��p{���D?���Ɔƴ
�����1{�����Ѡ�t +h�,e#���fi?مc��rƥl<z:��ZyL<�C��A�g���`]�&e����l���{�Ը�u|O��� �,]��.����gB��]�]X擨|���.�4�z{AWx�8���QL)�]�O��ۇ���/O�ׇ���������=��ۧӗ�-�Ĺd��Z,q��VC���)����R�����������,��J�Q^�r�6�ҮF�k�W����˲����h���#h�xNå�%��'ͷ�b^8����j��f/�����Vi��K"|K�3&1�c�	�RJ�ߤ��z��@M::c�o�ri�N=���b8�K=:I3tZ�V�*!&�lft�J�#ƶ���q����U�+T��?�����@g�h�	R씊��0�G���r'Cϗ]4�4!�|�L&�/���u�Q�;���ZǼ.iv��b�A��
;v8R_� c��y�K�
L���\��|g�K�x�l�,�؋���4C��}�}�B�ť�y��-�V,�����j�Jޯ��	3�,�бO����5�3���K��}ʷ�QM1����d�.������?�����n9�V`���iM�S�Kݼb̷�[)��:.��a{�o��0�zs�f�I�74[)�?6̥�9���ͽ�u۫0#�]���9ț����<��Rp���}!(��m/dy`̄X����k`�����uWG��%���V9K+r�%˕�BV�CJ\Z�?7$ˏ�B�KJ4K3�m�p�텢�g`��"���L�J�+���Ҋ�.��N;��pJ�K1r����B�btc�8\���F�p?�>c2aF��C�&�^*��J3t����f+�1�fޝK	:��o��[mtT_�t�J�f�أ|�c/����K3t�p�<g+f���ڤ:�K|��n���I�3��*_�	�|�B;��P~�Q�q�r��cr�A�04�5��K��]�H��\�?(.�����r�.�4K���@�0H�X�<������K1�h�y'.��Q��p1��k��,G�4�ë�"?��������N	�1�"s�f�ԛ��+��� �$�Щ7�W����_�4C�C/^��	�a��kE>�h�Rl��i��#ܰr��|4�:~��1���~��������o������y:����p$���Y�ki��P�a�� V ��)=���l��PT 5  n���R��55k��Ogf�5�ˍ3h��v���ӱǡ���5����Ӯ+�Z_���ng�3t�%�sh-@�I�;t�gX"�J�/�M*A�J�%��*��iN�������A)ӧ6�&�>}/A6���q+w�����=r)�y�ՀЫ����;�mnRGY|�6�co�{��NE&��tD:KY�I�etL�1�̌�D�cz�z��t�3AW�1�0.Y����|x�X���3��;Q�4��ۖ��~^�4 �=B���^C}(�T�Zͷy���pv�@��v��d�N6(wT��)��1%��b���ҥ7��$%-PL�ʉTϦ�Ac�'����L4a4�4N�Lb���Fˏ늦`�1!?�5 u)��ن��8�+=���P_�G:���JM�1	5K�=�w�M`ô� ��gT�f5v)�;���j���J�	g�g)x�/'4��#-t�@P�YJf�#�r���Hk�8�r��:�\i)�iQ�i�f�PN�&ųY�@�I]��Gι����L�2���DZ������l�R�z�@���7��|�H�#���.�����q��w[���	��ܶ�k�ɩ��d�K3��)�{)�t�e�f��)�VH�yS��fh�4楐SV2�I��Cå�����d��4#��k~�x��RP��x���Mq����1-&E˵Zr�o����7�/]���N�G���BE�mU��y����O�sR�E6��۩Ö"�0��t�4��7g(Xt����B�m󬧥*��Ҹ^�J�bh��1si�N5e3�^̛��.%����(��GBc�`F�N�g��f�V�OƸ4C�>e��^�y>�si�N}�sBӦ�G���%\
��Ĺ�t}Y��LH�mΣ/HQ��y��/y��0����O�S��t�B����\��sҨ($�����`��g7���Bt��=��8�Q	J+"wIݠޥr�7�e�(Xii�A7-��,�͟�T0�Z���Di�N�̴�K�l�����?+��ܬ�$�Ɂ���Ve=�j:�iu�-��P���O`n���A�¹F���3rY.,M��vP�����=Ĝ�?�z�Ø;�!� �Щ���v�\z�Y�9�R�U�+�L��T�f�ԡn8������ -02%��q��?�����A����/��N���������~;�}��x�|:�N�N��������n����^>�X��t��BW�f!�����/���#�¯[���ꢔZ����.�Y�[��Q�g�UZ��!��_��i+����������Z�׫O�F���uI#��Z�ߟC�wB$X� y}�`M��:q���G7u:j���4?i�����5�x��V����O�P�U�F��<V�zi�3*��*A
�N� ��k(F�L��4C_��y��E�.��{U�3�^�.�/�U����+_�����ĥ��z��[�!z�9ALs�!H3t�Q6���0�~Z�:��f�a-F�K�.�бO5�i�#�Ǆ��˥`�R�f�V�a@�&.�бO5�����l]^�f�ԧ̞�b�;F�0#�e��Jyz�`�lR�NZ��5a��r��(�3���z���^,���J3t�QfO�С�%�I3t�SfO���9��k� ���=k�=�b�X��/H3t�S#�S-�#�|�f�اF��Z,&��*H3t�S#�S)�3�e�t���و����a������S��R��RN���S��Z�� 8�Y��S2k��&�F�%A
�3eִ�X�4C�>eִC�yZ�:EQ̚Z1�(.��)�cִs�eQJ�IO���:��G��bvϥ:�);/��|rb�z��S+EG[��si�N=�k)v��RK���2�뚁�T����6:v�jZC�5�A��B��o��o�T��bL!B�4�L��[��>p���3�i��bC~���q3,��un�_(-б[����=�`bLR䇜4N��t ;j�=�:|�b��kn�AY�J�^�z�9��u���33��oÂ�ט�F�WI;��dY���3ДO�oP��̲��-i�S⧃6*=]�z��+���'�f��ޚ;t�c�հބ��-����%)��gC�ȴ�Y�	a��ɩr�V��G���|�����b��tz�YI�IoTL��P����F��^~.��?;S��t����}&=1q�����_ڡs��
&����Y+tԩNUk9��Jo[�lWn��	0�'d����G��X���M���ʾr���>��c��z�[u��3�."Ò��w���������L�9_����6�w��>d�{>��e�����g�dSXS���:v�_R�Ắօ*upTZ�)��������(�)�tx�.�$-��D��	��(��ӏ�Tz������<���(��ӞJ�׻f�!�y�1���T1��s��`�GC=bg�T�PD��l�1��7&m`Jm/�TMdfs�;�Ip{J��CO5=��N�ӫK������9��4V�u�b�j]e�L}��~�za��AqJL�A�D���?I����Ϳ��R�m�F�(5�;5"�)���Q�SC!z���Nm�j	&�T��.�'�1J��A��[B-�CߎPIQ4y~��Aq��o�q����4�N���Eנ�F����ct�@��_�۠7S�J��A1Ȕ�T��Z�o�>M��(j���wzgN%iia-y��:o��إ�����o�0(=��k��d3��D�^+��1�=�3è��� �HGűˢ���4α�;Iv6��Д�4�j���1Ǒqɤ�Wj��D�١/ߌ�Ok�J�B�����Q-�Q�$i�FE���:ۓ^C1o}�:
t�Qf�Q�"O�Z��p���~�����X���֪�T�4��;Rt�C>�k�*�?}��[��]����7&����=�9�n�KB~��Њ6}�!�b��'N:��,��>��:�`��L�k��K��7l�ތ+��P��Y
�Cc��A�NuK(&�jݩ�Y��?-�9/@���R�Y٠QG�t�԰�&�,�۩Qkӆ��D�Kj4!��
�߆Vב��p0�����PA:B]^%�����U�	*K�~���K�3��X��	j����(-�����Ԩ�v*{�I8�����Ғg��}��P�o>A�w�Q�g�����Ԥ���&��٫��ik�T�\�Im�FSt���P�?�ItH��e!���rz���
*r���AoB;�' ��5���DZ���	��]�8|�ʶC��=�t��~�H7 ���G�鑇uW�\���aMt��ѻz�2��Sd6�%չ�sd�)5�2q$}�Cc���푚BV��UxD����-|��D_�]"���FG ����2�;L��v�`=Q����Q^�:sCb��v�`=Q������%t�*01���| �Q���\����D�z*��9��+��9�O̧2�h>�����D�~L���o��tsm�	��z��,(
T�^���l2s0�(�Pa��(g:Jw��2V�L�mL��Jf�1��e�@�l�%�N�P)WX�y�-�>#4��+]pf�s�Q���`�5X��x��&_\�?����3R@�{����x�����פ�gv�[��~��i�ٝ���۷G��w{��)�[x�~�P��������      �	      x���ٵĶ�E���p�EpF�t�q4&J*�P=?�m�@pk��7�r��_��A����oj�}��_���
�0�?�g�?E���k��*�X9f�^_X�*��b���u䘵Te���Oo��J�_h_�o�O����B������U��%d]���W�)d����gUY�ګwYd1k���^=���F�YKU��k�*1k�7���¿N��z�#f-�Y��Չ�B� |i��*���|�F�J�r��W/U}�S{�cL3n��q���>��HW]j+D��^��Y�D˃<�=w�2���TA�P�f��R��@�"Ba�A�	����O��VJ1�R�ɫ��`�r探���4>=c�ޭt�(χ����eǙ�֩O~�j�K�إ�^\�Tu�A/8ZY����TeMy��r�����4}*��o��pGyh�����X�S��s��^UV��D�8O0�O��a?��f��C�(ō�^U����m=S:�䏪,-F�G��u�#�W�ţ����[c)=f-UY<Z�����uN)��u����b�=+?��x��<V���mL�@L2QI2Rt�[�K���ہ��@#�J�Y�{�2#��ͫ��Y�{ֲ���𛨤�~5�_-c�6c�R���W���e=ݠ�D!��^5�W�qO�!�R��U�{ղ�v��]UVf�ޯ�uξ����
{>�+�s�f������pV�(��[�G[���x�C��-�����x8b+/,S���6ɉ~`�`�o��Q3�G���.���7��ziO'��R�j�����?��p�	b�h�[�<��d��?�b�|mzUU��
�k��NΧ ��W�U�7�UU�Zƨ��]PV��j��
�5+��y��qBb�X�<�ܬ����w����-��&�V�Y^���x�>�����nȥU���7�U�a��f����b�AL[��Z����c�Ӗj4���PB�+'��M�����|
�Wi���Ğ��D�=�v�*ͻnڌic�̞U�Y/`L���y�W���@9-��%�w�h����f�E����Z\�w��L�.� ͖k	�l�HX�E�1�<BW�1l�����3�!����i�,�k�C�����)*�
sJD��L�s��U�ь�ڬ����S����C}Z�*��m�ޤ�i+^`K5X��,#���T[���@�!��0Öj0��ς1l���l����z�,��
��^A��F�n���
�5�0|�����`4��=1�o-��n����6�|����F��)	m��:{Z1�8���*��u����)�vUh�F��c;wL[��xil�x��i\�U����x�r�/o�T�!�U3!�@?d�]U$��G)���Ak�f�Q����/��v��K;��]5����"X#�YKT�,��cԨ��T����rM9�-�`U:s��Beg[���e�6��_������=��Zc�X����4Xe|F���j�)s���?S�ŢB��`�?�{���۫P��m3��&25s,͑mf���ߘ�	M{���T!ލ��<l�\pP�G9��<TK�X���x�"�	9f����"y�}��f͊b^W�$���ʡ��3N7>y՚?�o�G3U7�x�pE�Í��T��T�)��>�?h��X���x3��΍��t�.�j8��@0����8*���d�??P��r$���;�W�:ₙ���H!yQ0�]��x�k�iP�z�M*�ǈ���ؼ��!���!�0�x�h2T��J�.�z�h��:��i4�t�U��ƕ��G4^V�iK5o^񺹣�����
�W��>�$�6cZ�Z3�-�h �v��e_�*�iKU���<�²����M��4��y������j4�t�!�}���ٖj4�t�!�=��8�U����C,\��p�M�mb�e���9���0ڕ��!�=�%S'K��<D�2��WH^5�z�!�}�~yǫJ3o;D�e���ٖj4�nx��e���1m�F�솇HX���v�h�mx���}-�U�����w����
�W�NN�����bN�ߑN=��F�܆'�5��X��JSoÓ�}N~GëJSoÓ�.{*�_h�M���f_�)������SH���1����O=Ŵ�/o�T����9�_Z���m�fQ��N�5��9ĐE���6��s&��?�j4�6>��J{yϵE(,�5>+�j�K^5��iX\z�h�k.n��gEN4�z���ۼ�鲤W�&�.
*Mq��p�`tx�].����E�m?����������~&?�y�h�kp���~�JܫJSo�C,{���Dc���!
̜�
ztW�&��8��'Əv�Fo�C,{*~!��FSo�~�}��"�$r:�����A4�i���u���U�w#�Lp�]UZ�G��B�~t�����6fD�i�˛.Ui��� �2���/��T����}��戉��>�Ͷ��U�r��-&2���#�v��]U�(�hٷ�ns�����U��B�}��a>�Z�W��?˾�t����WV�;K	aN����ܛ�ư�R�j����m���4����R�9w�zmK픉J��|>���ɛ.�[���h�)�6����V�?��n~�������)m�!�FLk�/�4>���!/�b9<��<����:w����F���ʧR��+�^^��\�l���8��{�`C�}���<�-^5��D�=�0G���U�I�v�ӷ9M6]����@��۞��[r�ڮHw������ѫ�s�X��q�C���W�G�hʼ�hߖ�e~r�	��%wf^�İ��}�p�"��A����+
^5�z�~��6/��t��Կ0DU���DC�6)FM?�����6���O�RL���T�Ȝ����eN�sz�M5���}�g_�9�P�U6��˺@w#�WƟ�a�Ġ�̇��Ӿ܏%�浽��j0�K���y;��]5��*�������8�P�0��\�8+7��J�:�[ӧR%U��զ��s�+���F�Y0�ʙ���a���:��
oX�3�e��ֳ?$r��j~}29XP :J�(]ƯIu�U�
����ṼC!u��H����?c��З����8��K;�����:+� o�hG�`�1:��\��٣j��9����__�U��9�%���^�l��C��k�y�v;���3z�as���x���?�=�����G�`R����\�;�e�:�pNdW�7y���3��:N~����Cب/f����)D�=�U�I�1 �Q)��`K5��L#G���(!�R&#�(VǷ�UJ�m�U-Y$��!l�r��]����,����T�q���c��W�5�45 fOI~ƍv�FӴ=~��?h<������i��ə�qŁ1k�_�U��Y����i4�?d�]5��������c�R�69��#M��!v�h�15}���4��<s�m�Ɣ���a��ǜg�UP	���`�SԼ��j0	���`�SB=yǦ�kjL���C��4�tC�>l�^�v��Y�P�i,�����2/s�mSƛĔBO�c�R&��Rh�7����T����e>�^s���})���Ub����<��/���8���h��������Y�����{D��O��D��`^>f���F��l���w�ͩ}�[x�`E|l���|�+��h��WPP��Y�9��њܲ�v��g��W��墍���m����^5;�v��w|i��m��i�!�/���	�g�U�38�W���G�eO��r�]U�L�a�졟dW�rK�q������Q5ZV�p�c~y������HX�e_,9�F��o�ca���ཻj�&�>.��c��j�.�����߹r�??��}�{P��%����QU\W���澛x�����Ué�A�q���r�p�r0b\�?�9��3��1���T��	�Ƚ1nߣ<���u۾�����)�dp�j�)��o�?�����pM?�/� ��k�t!�Ss�w*0)O�����F��{8�M��*5��4\�z�hvV�iícT�a��(=�͒]�z�hz�V1m?5{T���k�����M�j�"�P0�5��}�8�F���K1 {  ��Lr��w W*9P�ؚ�ZO��>�FoW�T���Z�'���=;_����<����~?�W�ɥç���~?�\��ޥ���-�5n�Dk|{9���������iȗ����	����xZ��6��(�o��q�.|"����L���U�h�j�*��RL����j�&�� ��i1m�F�;�R�s�m�����hC���9�a�j�)���~ۗ�F[��P<��9��wgp����[fY,��J\rx,��.JOjb���=���9�rR�����Xx�w�'UhE�m��۾_��T��w��z��[�ݪ�t»�|=�kw]z����}��a�
�<٭
M�����þJ�*4���[_�EH�z��G�*�t���}=�i�:��A%Z��Ǿ���G��tV�����#a������,�zt˜O^İ��4�yt����G{�LӉ��q��ѯH�U��dw�80{�A$~���4���k�zr�P�B��+�Z��u��X���^s�{R��u��Z��G��uT��u��\|�S��b�CeZѺ~_/~���N�д����Pz�UhZ��k�{�4�j8�BӺ~_6~���{�eU�pU`I�4?����i��Ѕ��K��\�*w�ƻ�݅d������줹��T�TZ��	2�5Xr�D ������7�5������ܝF��|к�-��\^`3�Y ��r�M��b�i㓨�%��W�ʭ6!m>�;����݊r�MD�?W1�4|4[�C�۬#Z�Q'����G�f��Rk���3�G�4C��9�U���K	��5F��<C�F��ol�h�q�/�% _��F��R�V��fH�P^�s�Fk�m��c	*T�&% �S�p<NV��Ѥ�k_͆g�n�j4)���V�\���<�P廎@�'�#����s9h�M&�|q`D�����d��o��ˋ.�X2���X#�C��dz�w�����k��4��m>��|^o�Fk�m>�=���lK5������Nk��R�̔�
5�/�m�# -��1�P5Zo�>��ZP{W�6�۲�����d�F��o�G²���mW���o�G²op�]U0�4���8r��߲��e�s�h�-��������񡢡;��È��-�p�����W�F%�Z����6c�R�ŞV�(xXczc�jo����Qp���]�{�h����}iom�T�����FD��OBC�h�pGEfL��F�*���`��o���!����G�+ʲ�h<�ĴK5Z�^�!��]k���tt)�Z�2l�F�ѥ��&7$E0��cK��5y�:��j�����E"ڨ|�8�-�hS�4��7Ө1n���.�SQ��֪\��$nv���\�����sx�a i�� ���)�ʰ,y��X泵C�y�aE��X��`�ʰ*�T}\�țH!�R�$�ڏ�M����9�=��U�''��Wh%$��$b-Uiz�Zi���iK5���Bk!�/��iK5����c����4S��鱍��S��.�h� �i��nL[��4A6�i���I�c��ܒW�=�W0
���rY*8�|�]$\c���������E������*{���t}D�T��x֜�o���Xd�#��6�OIM*���ɚ0�yD4�� ����^�ɚ0�zD�q�G>�&�/����~�xu��"S+�O�%_�@�*OC��Oy�A��C�C�.���:؏�'U^U��2��U�����	_U��2��饃=���*4]&Z?�t���~ʫ*4]&Z?���g�%_U��2����=���WUh�L�~��a_�����ݼ�Lӑj�����'Ĵ[e����ca��zM�_U��H5|,,���ݼ*4��������nUh:R˾Nxi�[��T��²�o�x�������Wsbح
MǪ�#��
�|��*W�EO �5�w<N=��J�Qa"���!9Ui:*�C$�}���M�� �u�v��?�ğ���mu��7dYAZ�E���:��µ�1{�j��n��9BV���MU���Y����7UY�CV���.UY��BV�/�S�ő���[s����D�|��y#җ��1�/[^̛���>�δ����[H�U���s���Þ�J����eOs�Ҵ�X�|��g*�nUiZs���=\G8^Deiűv�漽3?�����T�q������ �N�:      �	   T   x�3�4�420��5��54P00�20 "]daC+c�������!H2�� �(-3931�ˈ3��������p��qqq )�(      �	   �   x���;�0��)����w׿�ZDGD�Ѧ���ĩh-�jF�� �G��qx@W����T�X��6�ٓ>G]�:z�6q�f��3�k��;H,zr��zu^A:���Sl���#�9c�{~շ._���3�B�      �	   S   x�3�4�420��5��54P00�20 "]daC+#K �3��4�0ɺ�'�p����\����$j���WR4 F��� �f�      �	   �   x���;�0D��)|�X�k;��ttH��&
,,'�@�>q��E�j���Pe*F�5��P �%5�ߚ0��$��Nz�L���������c��}J1?ĩ}wO�;L�dC��/��_y�3���.����'Xj�*���5��BqR;��M���/�w=w      �	   �  x�]�ɑĸD���� nN|�;OU��s���+.I A����퓟�����Z����n4
E!��,�g�U��8���v���
Mi������"[��g�&`���?���%f��s���̟������w����Z�O�����{��~�׬�.��Gw)�EU)+�M��ֺRA-u���/���!M�6s�9�y�2s��mQ�biKIB��ZLzS2 �dB��$^b��~ݠvٝB�6�@X7�@8�@�8�@��?�-ؐfn���s�6PU4���m�Z����$K�ٻ�Ejp�CLɆ�5�;<�U���c�[٠���ʜ�Vjmޞh�f3r�j<��g��:�H�2,g����.��� e�r��9O��\'c�~�����-���x����k������$喲z<�^�b��BXyy�檮�4;O��� �_�\˔�g�f_����{����f�{�Xs�#��I�n⠓	�Y�M�f)c�C-`�ڌ����j�����uNQ��0\�	k.�9c��P�8k*a�k)A��J��6%̵�0�$�|Ak�I��Y��j1���z@�h�@bm5��Pi�%��c+��i���e�#���*�	a���^B��PEdZQĞWn���lo����Ɩ4h�g;Y<M��d�{��96C	)<S{��S2#ɬ�P���H���ml=��|c�ɰ��ç�Ul�*$��9m��G>�;���m�+�%��k;�0{׼B��м��rD�
�Z���
q�"��٧V9ġO�s�C�Z��>��!}j�C���U@]q��k�J��J�J�J�B�+a][�`wֵ�ֵ�۫�KU1DZűD#���w���2ו����;q�7�� M	���>%�H�62�,�|{�P�Wƨ�ѴCO	W�(⺰����e�l���6�_u{�fΖgo�`��ެ��l�,���R����L�7Y�e:�L���+L�����:Dhu:J��ʳ�0��ӑ���9�զ
�!H	�.O*�c��/��0W4%����0W�K�i�McN��T�$�G����NV)�.O�M�d�"]	VMe�}��q�F��@S�&cG�-$rC!��H�
'�4rJ�8��Z�+���uԏ\�ddj�p2t]�?��"]V�6%�b�,�|YHE�+�E4ZR�\Ac�@�V"�(,2߽'�,m�ls+a���0���BY˵Y��-15AY�+A�^��"� 9hb�f�X[{�y7%hު��&�+A�VKs��V��U������8�+�俗4�W�-&��]�7�[��7w�߸n���2���s�ӭ�u������
�@q.����]�㻎�]A�_�~����&�6�Qc+���M��r��[�=9%A?.�D�����&���ʒ�����-"�]e����b��ܺV�<!������-���n�y6�U��1�2��4�a�x=	�Ǟ;�E*˧pb�\��R[v=�<[V����n�_�:�����.UiQ��q�=���ٮ�!�ٞU[1R��jF�W��8���Ɣ!�"��o��G�Py��$�a?j�lv��i��ъ���fPe;<�B([?��
�6��7}��ʦ�r��4}�� J�W9
�4}�� J%�ԗ;d[�kP>7��wU�E�^��y��#?�ҫ$���9Q�+�Bz��(2�`��qN�J��qG#+dw%h��]R e�
��C��z(�2TP�� �4%(LUH�y(�W�^T�ՆT��6J��-������߿X��[      �	   �   x�}�[
1E��Ut-I�iҮ�E�3>@:�(���uDG�|�\N��"�dA,�ȏ��m��q&p ��7���Μ�q�A�3[+}���m�E#�n���Aw��0B����u��%��G�P�:~K$�D�q��	/�X�kѬ���>P�F�P(`�k��t��i��gHI      �	   �  x�U��� E���L�IL�c�-����#���v��̾�]?��V�����c%�p��Ͽ�^[G�(86����U.�H&����|�^6g{+W�I�ւV�!<�3J�V��ɣnc�
ȭ#7{Xl�E���²q|��"��)m7����}�����Z��b]!��6��-� �bn��N�a����;�{��7W*zm��I:|�3ܵKK��M���c��P�h�Ӆv��1��]w�tn�Rx�g3l�P��̖-�{fۘϜ���ԂԒ�Z�m�L�Ŵ�n�tj�Ji�3+�l���,�C��:W�t۠\�щ0��f��ѿ���ag�aY�	��rg�Ŝ������ֆ:=��X�'GR�^'֐��5�!��u(���1�0hgΡs,5]L�b��htu�	��Q��m�c���}���(���m�2�z��@�ӵ0{�a&�I��HЖ-k�ɠ�S�{@��֞?B�G�� +&[��mBۂc�d�h���JJ畩P%1�9U�<MW�o��7)C�V1ꌺ/�:��`΀��:׉�nNO�I�r?bL��Yz�r�����XG2�-��b��f����N�392� �l�$�Lh��J��z,&u1����f�2v-c�2v-c�2v-c�2v-��s2��8yA0�6�&7��f���ds����,�M�s�������B\��Yoo}/����j��gζ|?�E��J��r���f�u�ת��Q\ݵ��VWw+�5Q�5Ӄ�
�3<�𼦼�g �6w�;k�R�Ϭ�=�#�(����J��{�9�ν��N��-�]{C+/�K ^8��N�i%V��<򸸟52�.�C+q����X�.�s���&�
l��������7$�d�x#%1�lw��?l����Y�	�v�|1'�$yZ��F����J���      �	   �   x�EP��0����:��tEB,!��KA](",�=6j�r��ί &�/�yy�kn��p���E�n��rn�|TN���nj"�l&N
ހ�B��g��J�e��.'FT�UR0U!�#���Ev��/B��D��]��wE(5��w��])�����5��JmIa;\�P��}�t���h�q _�lGm      �	      x�34�4�4T(��)Q((�)N����� I��      �	      x�3�0����� S      �	   �  x��Z]sܸ�}��ӵ�4��&9y���&Y�ٲߗ}�f`c9Er,���4@��Kr�*qIe �ݍ�ݧTi�D��l�i�T[����Y�3-6\cV�~�eRn���ijtF�BE�D���E�0�m9�Ox�2,�u���\}a~|CKn����Xf�On�wn����b�v;��u���\�G�G�ѵ~E��,D&��C$t�}9���˒��|ꊺ��^����8��8��c�kؾ����CѲ�|�O���(�-�
7��6�l0	O7��ZB�*q��r1�eV��Jc!�,���[o1��nD��[����b�_����<z];�����h	�%����xn�.��U�?ѯ0�1���x$��-`�]u�0l�{<Fk;E�(��pd�M2T�bJm���Ȭ�f0Y��$I ��J�� ��p��ǉծ<�����#;�mW@C�⟘`��u@���ɋ����{Z�eվ�;�9�Q7�s��\Y?�[�^�Llԫ?���m��OX$��ϻ�nZ�Bo�x�`�D�ܣK�$j��B��P7UD�;廜�^�3��ڏㄷ��Fhn�(P��B+큂���nx�)��Ptğ������дqPy_T���Jްv�νkoL��/�<�9w-���[w�����̯�|\����L�J��Ag�n�/��P�\#��V�8���t	}<��?�k�X�Bv�lT@�H�+�/�^z5��l9�2�Jev.���dkn2!F�<{9E�*�l8�/&b��Y��i�#l�f8��y�4�VpDa(�D0:b4b�L;y��Jc�xh�:-��V_sD�Sq��n�w�P���W���T���o�.���_������-�sÃ�i89�$I��FɅ�`��hb�e��&"�	��L�*�n2��"Ӏ��ܔ�w#�c|�7}4)��H�A8�񱽥���d:�03��q�q���l>;�Y����p����<���Ǚ�D2Cr����U�.B	��8Q�I��؁�웥���Ih��v2���+�r�z�ZV����tS�:vT򒝀������Ђ�< �����=BpS�n[�?������hk�3 ��ѻ�kZ�S���;�m��aU0������_�Y ��A0��(b�%|FVg	B\�@?1��I�i\U�t�b�-а:�%��#6�4扐\-%���g%�'���ɘ�x�'�*�r)���F�4KԒ�`��#�����'�sC���໛�tx��)��������+{R'5��d$��i�v�L,3��V�`�-^�*��l�@��j�@Ó���gO���,"k0bcl{)�|�-�B�uα8�{D���e3+dc}��]-dw�"NmfM��}>;��H����U��fI9�x��Tv�!*�*8 ��D_N�%���TI�R��`��yѯ+�쳘K��*��LV��/g�ҧ�Y�JO������K�,��Tq�ĮH?�MH�,�)x�jڳa��m,�/���pW?2Z8.]
��B[00;��+�S�n�a�3�˰V�	GG�e�<ɍ��:I���g���I�X#^����~o<���P��^�H���dG2�[���El^N�%����^�ܮ��+ ��Qzm I�Q��q,3����
O<i��� �B��&�˰�4�'�]]!}���8�ͷG_�D*J��y� ��Gw�#ɚH�@U���4��B����(�����6"e��!x���V\�-t_m\��~8l��	}�� ��/���m]�T��/
uVxF������ ��SS�(P�8Z��<Śo���%#��ck�ʧ��ݻ����a��[�u�F�(�[[�B�~d=O�����Ɉ��Y*Uu(���}�ϊ��'��2O�}�{�����i'�?;n��v8W�p�UM���}��i���+��z1���re�dh~�ӹ,���EoKW�r�u�(���_dbl��P�,6�A���$�Y:cȖi���ս+JO�VY~��/,4�hIo$�O�~�O���x���P!ۥq6������	<k��|+�ã͸� �[�cm�4[ ��s̢��p�4��Tu5R-h�i�4͠�5ч�;5oOnW��c����c@\D!@� �4� &���B�����Z�/3@�u@,�߼���� �(�)PVt5sy�:<�??�� ��A�!Y��z��w��d��9S�N� ���^a�(�Fo�+C
�R������O<�̠3$q27����yB�[D�j�icd:e;���tn�'|��XG��ȃkء>7ԣmOHv}�7��xl��r\U#ԗ���h��m��.a��]QLU��i*f���D�Sc�\R��OKm4���6=���SJR)�!~ɻ����TQ]�<R�.vn���j��B&,�raQ��/c�U���$����,v|�ʮ�QFP�mVD�g\Փn�Av���n^�b�=�zŤ��bHڧ���(��
�]��v9�&�8sT��.H]/C��!�zK��$w��D�O�����c�s�+���X�=A��^�M(f���wF�Y��Z,��}�[��ƳТR�EF�i���D��
�z.�Axu!s���3c����%�z<�)W�@�%dl����3d�I����|D#u����R̵�����F���O�Όn�l$��ܪ��Vxq�é��[L���0ń�X%(���I���3H�<��G#T�����B�K�I^��Nh�#a��;��z7j�����ߖ����@.����������F"��,U�{��l�	��n�[�cZm�cefg�a��r`�(;�{��C�t��+�|'��<W{�v-���+UW��GGm_�GC�T�]�����vZ�H�L�I�r�|S25��f%ike�-<¯v�y���e�|��/��G�ã�z��0{9
ӯb�q|�8v�}^�w]����'�G� ��`GԚ�u1u�?��s��n�����ԓn����}� 
��kGN7���VL�G�}�&\�N��)�ug`#~|�F2}�V*w�,N��~Qy4]� t�=:Tp0�V�d�j��kb�f���������)���n������ /�Vr���r�p�����j3�c+Sal���ǆ�IW��|3�P]`&�/���/A��_�=냊~ܷ��C���Q����UܵPl�����"���d���S!&|)//�z�"��#_&�\Y�g����䀾s'�H�{4o�~r����f�88$&VްįN�]��l����.D������@A�7��j=A|I|t4s^H���/�YO�ib�
<�E�(Ni�یO�����]�m���}���?��;��&/�6$%29�xA���<�&���6_��&]T��T��,���L�n8�m�J`9����?��%��[��8��J�e,����!��J@��$���Um�B��_=]p_]�]1��.)O,&(S# [��.��P/�T�$�[����jqm8X̏O,��闰�����2�U�`��G�O�$2[F�`�t&�������J�zm�[���t��yk�����zGa����t
���BS]��������=K�\ڛ�YDS��2��M�� �� )�.���e���n���BX�d��71��0I/V_�k0ք�Ui�i�ȫX�Y%c�%(�X�Y�����;��7�F-_C��O����L'�K��K>7ε��=���� É���3��M��M#�n���ħ'�|P&��ˍ�3����|r���Ը��9�WY���|*�|�A0�+܌
P��I�THi+�f���(%�Ֆ�`٪�w���}Q:z��/�?�o�      �	   "   x�3402�4�44�4�42�42,�b���� AbF      �	      x�340��24�4�\1z\\\ $T.      �	      x�34��267�210����� ��      �	   Y  x���]��8��ɯ�e{�?0��uV����U��J{1r���f���=�i�@����xm?���9	O!jK�rDy!DA9&B)�%��m�1D��u}����~xo_�����x6��4+ǹ�Y�/	k��d|5�ゑ_2$�y	��LYƮ7�kF۵�}���*	�P3�T!*
"�qƘ"k�51���w�	hg���������@��(�,(ٴ�D`AM���x���O%!��߿|JN ���m �3�Di��Q�ei��K�m���a�\Ԝ_cx��	Fo`�-�W�t�a�т(LU*�l�Y�I�|��ݿ�X�:[׭�f���@�m��:+���[��N�.�M��L�U5��M�E�R%�[Xr˲����c!��9��S���t7��@�7���/����@8��и��^�{<�>��*�TL�G���X�� ��^Pp��l�]g�?����o�tf�[�Ba)��b�^����\�j�eh�n�_��׵=Ńwݐ��su��U�DT!$���]�o��������׮����)���r!��E$�	�X`n�ט���h�ic�`�8̝�v��T��;�����8�����p�%*-)X�ӌ�<_�V�1���9_�^GN�tx�_N{̳�/�㨂̡�
�����&���u�Y�^l�����؀«�U�j3�*A=����4u:D[�������og�M�yP��<h*c�w����0��~��Ҳs����T,�΍l��|���^���ܸc�?�@
w(+�<��>�ce|	�XV������B+��&߃d#�e!�н�=8_�����d���{3���ɝ�g��l��	�      �	   b   x�M���0D�sR�D����p�D��]���v5��5�Iतйm�rY񆚠Ql�F{q�m���W;h�Γ��?���6Z�Ql�N{q����y����+�      �	   >   x����@���Aq��^���he�ޑk
,{<0rW���-Tܰ!����K���:      �	   "   x�342�21��216b mb�ebj����� G��      �	   M   x�3�4�4204�50�50Q04�25�20ӳ42144
��MM�L��2�f��������VS�%}KR�����qqq �+      �	   7   x�%��  �7ƴ������x�=�L<�ҖIIH�������|�~�� W�
-      �	   (   x�34�4�24�4�2441�2420&\�Ɔ�\1z\\\ k]�      �	   !   x�34��210�216�211�213����� 5��      �	   t   x�m�;
�@���9E.�0��}Զ`�bA	$)r|�e�����N;!���'����Dd��v��5��1���n��
y!���\����s0�bD1xto*j(N�����<�L ;�e,7      �	   �   x����j�@�g�)��N�wl�N��u1��!�!�>~��B����O�Ic!�-��iE��J���m�$��C5l��t=�̿�B�uf�}�g�:z�lm���`���G��~ty����`�	������|�3���{QK�%�&r�,y�J7��?Cx��ﺫ�*I"Uf}{��bns�J�)�S�D-1[���|��W�O��f]      �	      x��}[�9��s��H�<;W��[͓��9��vec��ve�	��p�{���K*"�"U]N�`����c�B��DY6iƚWƿ�������	!�����H-�ͧoǛ�7w����~�����b��#��s�����L ���+H[�>]@ځ��x7����뷗���}:|������ǋ߾�v���m��>|����l??~�~�?>�����>���`��]�LG?����/�4�wu���R7��-#)��-�18���ջ3)w�p�S.��s_����|ʝ���*��ۦ�\�lݤ��9Fݠ�I�a���0f�>[��-�k�]�eĹ�ݬsna�.�rvk���ن�"��������f��%8��)v�_����<� ���ݼ����)_p�-ß�j�P��k�� �󅉻`L��%��}�n�r���!�gJ�.�~�i,Gc�)�l�}��M`է�x>��ܬ��a~�/l�E�̢�F���q<1z�-k�,�ڬ�ϣn�A��b�����U�"�3��}C������MC�'��5Ӗ�[�.�LNXW�g���_7�O��-�Tt�O_����R�7�;�z�	 ��/��|��������]�u�K�?�l^�����p����� >p��\�>Q��BF�a��Rk���W����X�,�z2ٚ�C��#�;F�B=t�-�.z���7b��{�`i�vѫtF��F����!��f2��'�"���}y�{Cv�8p�������v1&g�fi��f���]�m%6"2��@R���2��O�b��&+H3&f��`7�۩�Næ��Ⱦ&�D:`���m���* �%��Zl)e��Oj{c�&q\�B0ɋ�/����ƜD,�|6���l E��+[p�]���B(�E�ywM��f��J��O���i��������������|H�p�x�)�\�,�`�����b�^��YqX��_�|�������x�	�]��l�����D�~?y��蓴��~��
�c<Z��UZ��&pw���.���.-��WOzÄ>|��u�I�Ne�&ၜ��U�f"�,�E�R4��]����.8�٥���>=�F�rv�FM�F:h~��zވF�v�"X8ռ�34���R�5h����wK���t��r��Qc$_�T%�"#H�kvh�2�|���)k|z���5;�}yZd��E�	1^s,q�ys��0i�&f͒˾�Y���U����g�:
ɖ��<��X5HA	5�?p��ye8����^���l�Z��H��ಣ�Rl�*B�K��Z9M+�w���·JE�V��'*���z��V�/�w���_��ǚ	Z��R�|��.�lb�[���n������B��5/�r��)p�)��\QW���w�5���9ъ\v�����o�)d+|I�_=��E��A~�.�a�Z�"K�v����o�H^�?���x�N]h�K�G�H��x3����.ع���}�I��<��G��Y�=)�̱'kc��y���t2̾�x��N:j��r
 \p�oҲÎ@��X�6�c26�ù�G�t�hr�;R�����Ȓ��ε�Wc�bHI)�F�ELn��g7���[1ͤM4�=��Ԃ�sl�u4�Δ.e����Z�P��&�z�F\�L63�<�	�[��G�������P赿ݾ�91G�uɼM�KFN'�d���K;��z���������ǉ�gy6���첱(�Y�<ԡ[ڼ���������i{�@tm+�8ߥ�nL]��C�z<|x �x��H{��|<M�s�J�d�^ɘN��(��[�"�>�3����4�l|�"9����]f���a��j(����/�#�{?ST�O;ل�W�<`�{�����p� �]nj5�瞤�����Q��nN�ִ�ᴄ�Y����pahmH; �q0A�|��e)�^�$T\�e�2gYw9^Xˑ}�z�Ĩ;\붡�E1�������l�R?�R�ҏ���t|�~����?�n�{2�7�v[���I m>�G@���`�'MX�G�.��՘����y������؁���-\ǂM!qw�'w����2�^8�O2�������H}H)B��R���D��������"��i��ބцAI�wг��8��	c=�a0���mxZi;�9&�<I�7&m�&�EӨ[�I����E���x��°4�;�\����ۃ5^ز"�a���0��������9����ͯ�p���&璖�m��x��t����}����l����M)�Ȩ �a��;� ����4��D����c��ςL��e�9M�V�H��(=Aǐ���s�
Z��>�iűZKh����-�T��N��!jY�9繥QU:����t"C[oMm������"��J"�kEj�8!�fˠ<E�i�fP�Ri�i��(���i�6;o,-��,-����q���{���a{��z��h�2LF�L��(޾��t;��r�>s�CQ���#�A���~D����֬d�j���"b+oI�[
��qC�3�o�z��.wU_�%��Ѩ�E�	�ū�+ߵ�VmYZD�����\��>v]v]�S'k���p��	�ӷ}Q�=��K~��VK�n��7o�ti��9�������4�hDj޺(۳l���~�S��߬�(��3F�#PԢ4x�+k)�/�4���y�4������=|��/&W{��_��|1vG�S�����y=�=tƧ�#7�f�lG�w@�h��>g���3�k�I#�}N���rl2}pP4��;�J�$eg|������7�]?�b���?D���*����f^�y@q����_�Ӽ�h�}T2;!�&z�V'vw�Px�V��$���Y�lo�����;Z'���4��e�jr�5�d��=���Rzl�l+����-��v�R��s�J���X�RIY|�Y�C|�Ek@	��e��1�F"/-O��&��֐ɡ���@
��q�#t*,C��>�cR�����"���a<�AN�/�n�l�������e?�ً���8����'p�8y��ƌ�䉾٢��O*�e�D�3���}����RZi���fVY7Z)3��C��f�0BԢ�V��~�HIgPZi�Ƞ- ��t����8�Ρ���\j�;f��Nuu<�ܧ w��U:5�pN��r=���
�D-Jm��"n�OO�!xz��p{�;�?�a����=�n��>�~}��n?���ۇ���L �`�����i����_�}`x	��J��X���S5�t�Sj�iʊk���hbv��o��n��~Ͱ)$��7�Rp��OQ�Lq�w�ˁ��}��멧�C���%�e
�7f�{�k�t�@��pf�1�t:Bɞ`��kTS�H���>���{-������V;��J�����ϒ(9�	&�V�F�$����V��*>����hS���1�ٖ��q���'ҹ7�����iƮ�2��~<N��p���^dTr���/�J��s=��'r�����.�xr7�'��vs��������EOF��RFw�?Ip�Ҟ��UO��N/�ذtza����ɲ�3�Ǒz���,��Ǉ��~��G�X�鴼�d��S�4���Sm���Ie�g�l�'7
��m�\^^�Rox�4���q��7]����x����4�O_o���[Ո��xC��ԍ���\9���߼�����"�]t>��wB��F�t�o_��|Et7�(��Ήm��ݴ������+Fl���\RO��?)J�v���),��ş�y�(P��`�1o�~���I��A�<�-�]vIu=��١7�j������-*��$j�CT�����<q�����3��@."���,�#g�89�q�t9�|4('��tb����~[)���\����7ߔkV�Ȏ	�
D9�9�]n[��G_�o�������*en�Sa3%���'�Jh�L���ϕl�n�g�ϴ��2���2���!��8��ԍ��vmC�R)�I膝)�Y���� |����	zo��P����"gV���e�8�8�9��?(��8��*�+��|>��b��    fA��J4hv����%gƄ�?Q�3��.$Xa	*(�?Ч�R��}�-��Vs�R@��˷G>P�N��t�03�=}U&)�Ϫrw�����i��.6YJ�,����8RJ�ye�p�˝@.4RZ�W�$w���I9��p��螴���"���0(RZ�_p�J�v�vs`(O�H)S_�)�@���@�������FHi�~Aokܮ�}�n�5�½�&��]j2����B���`{s�^5���ĉ�r�6�-6M*�ML����h���A���+�6��)�8��/��m��GpY�z�#;�"�M����p��#��]e_0�<Y|W��^�A&�#E+�$;�M�G�˖d����
M�/8>�P�Jv���\�%�p#��v*�N��|!��Ss�K��|���ZjT�y34;��C���v��Y�_��]n�g"��3e�G�SSH���7Kq����|rv�}{7sV)$�DߣR���B�R�1�ۻ��V٩'xF�B�v��Yo�z�"��Bࣃʡ)����/���շ�<�7󖜨�T�9�_���s!�++ب+EU���Xy���R�,��oݹ��G�[�8^tU�3_H/*& _`�B��oǱ��e�q��N����>I����GYKBJ�zN	�85�zJ2?#�\=�CkH��g�Jx�q
jp'~z��9Alu"���v�L��ڽ�"����`_h؎��/����������I2�f�x��2���a��OEb�b&�� ��ƫ�q���)Onn��`�
���B�
w�c7�}�lm���;'jlHia�à?a�U�F��	�Uiaփ�����9Y��;1��kJfvH�~�:J'�����1Y������f��r�d��i���F3�ϨFZ��}�2'/�����.SV��0�d��#�|W�ʌ���f:�	sD%=02RGF�ݥb��O���0b�,/hHia�Z0��G�6�w2/��Xee )�ٲ6��Ȍ�;\RZ��%�b���)�9)-ܫ�m����$�7y��Uɶ��N�⥔�W&�b���_�<�k���uɶئug�l�Q)-ܫ�m�M�Tp�'����Uɶ$<d_���]�!KYJ����b1�M�jD~[n�%�-PyG���v�R&����4�-�;RKκ����A!9a���)��u��K�;5��Ts%�њ|T[��"�,+Me�fzD6�HJJ�:S������RQ�{��U�2K+=���٫VZ�W��,����6o[)S�4�Y�iOw�#ceal��{����L��Ρ�䍴p�2�YZ�	�+�1RZ�W��_T��˭<
����<rWkW8k��'�ع��]+}�)���u����hj���/��k�����|��/���`��Jv�����V�au�x�5X�ؑP�1m���RKmdyƛ��~V�)�?�J���������Y�Z�� ����W�2�6�0����(���z��D?�r�g��t��;����Q���܈i�	�]�@9��=��~*�����U��3��m��J��;v��3�&��½f�p���E�,�|kTi)�����R����%U�����R-��s��ԦhygЀ6�r�'� ��� j��?-�5׌w�g��j�a<|�ԫ��:���\b.�g�ø�[�ה���Q;��jR�5�%�3�b���ŭ���GO][���:�1�����igA���4A{$fI�{�R�ٕ缩BM�\���:���jS���I��>��d륧"�\��9��%��DL&�A,��%��ܾ挴kD�����UZ��4�/���1C�R2\J�~J��-�^JP��d����ceT�K�x��|�S.����nF���cX�T�����yRUZ��Ē�uZqM9C��6�<W�ρ<7��Vj�1.c��#��nAYG�H!#,���c�O�j��KЧ�3�q� 3����]Szs ��U;di߱�b�Ny3Z��Ʒ1h�s�\��bU�^�$���[�,)*��J����#�O<�'o�����k�~��GtoR�sWi�^�������6� �|����sw��ɥc
2���C��Y��;M��5E^A��7�a}n�)���/�n��J�=�qB�=�&_�b��<0X"^M��6��|s�W��r���ɪ.w+-���S��3}t�3�G���ݝ���]�l��A����"�����>)�@+-����ғ���Yr��;/�kdI�K%�ɾujȜlz���	n:�"+��v�ܥF'}���u�
QEY�e_L�:��� �fVN�`%�e�F��u�`��3�W3��½��KMF�⊴P�Z�Q��{��H�I!-������{Z˂��Ǐ{���6����o}�Iʄ_��,�O_���������=~��������_���ij��g�3L񖝯�_�����SK�ݒ�1�3�1���D$��Ur:Ȼ@6�$�;�b�4��ê��.�v��L
���$���btk}��6��.�C���K����Vl��r�Ii�^�������hE�E��UkKl���ʓ���W..��������B
F��i�^��D�r���ړ�U�K�=�lщ�EJ�*��	�]=�r�%UJ1��y��Ҍ�ވޖ�½rn��lF�^Z)-���vk�*8e�Ii�^5�Sk�fpזU�L�rn�֤qEވ��� ��½nn�֦��Ɉ��p��۩5i���̞Ji�^5�Sk�\)(�w�rXT���b\�GK�I�ѣs�g��½nn'i�&�DfU��Us;I�6��S����P���ҢM�贁�J�z�ܖ&3y�;I����p��"�6mDw4��J�����I����,y+-ԫ�vn-�7��.��ISE�a�ʹ�[�6��Q�>�$-���vnmZEwֈ�NEZ�W��ܚ��Ü>�$-ԫ�vn-��MJKйjn���yAy�Tb�a�=u߄�㋽�<���Wk����e�;{�e
�b_5Ώ	�O��G�Ѧ�r�T:ҕs �I��s��<����jC���jV���s{�tTC��ܻ��ڥ����6�`�j�p	������G���2ڔi
��.��n��87���sN��r��\0��inkӝE;���h�,�Ok�3��(��4�T)-�����Ť=�
N>k����e����>�Bb�S*~���5�#��T�k�N^��X?ǳ8�(�
�-�:ku'+ip�s0Zu�A'oS�����op���-�Ec
��w����z��Nֿ�Qf�3�2��d�;�S�3^Fv�Ѕ-�b�Zq�I��&[>�Aבp�k�� �)us��k��pR��0=���Z�>hs
+��P�l��������~i3�ü8
���bg֯�f���|�T�����i���@�W=[�
��$����1J.c�����RD�C��#w���k���(�r�U>�N-���M�R��/��<�A�4ը3C9��U�_z�U���1�\��9�u�U)e�Y�n�{��x�x��t������i�/w�������ի��7�۾?l��\3v�}"#��~y�7�wǛ����~�����p?�����~|x��������������Ln�7�9�#�Y���X=�y�6
�] Jϕrq�H���X{�,&�5d4�\ڥ����V5�6U��3��e[�_T�H�������Z��s�t;�x��ݬ�8����8�ѵ
��0���q9ח*�
X�կQ��@t����S�t׼*p��Nb\Fui*��ŌM��Fu�J�0�ᭆ���;��D���ztգ���I��1Y~>��_,��v�㚝v�ߏq�H��ՏF��(�����1�whw2�RO;RD�j�}���� K�<_���g�~HǄN5���on=g���ry��_"��.�;�ؓ�ٞ~������L�R��;�s�`����Z�Ça)��v��1������-o)wg����ISd��v������_������nE�:b��d�,g?@�L��=ƒ	�Ҽ�i������;�5�6i��"���9�fm�a���\?�y�KJz�7��8�N:�Z,�5DU5r^�<}ղ7�U�~L��2���BKDu���%����x�����sW`�!2X�� R  Ǻć���g�sH�\��f����f|�+O���0KR�:�����Ϊ�C�U�g��t��39�����bZ�v����7R�0+x���Kez���u�.Ҩ��0�^F��<��2�Պf~x�4�I�ħ �M��M/ךA54���dL��1�aͮΦ�[h&ךQ3����Q3~ưj�C�/��I���f�<�5������#M�4�j�v�U��Fؤ��YFZk��\+F՜��idx��O(�M��P��Ũ�elP-rf�V�!����ŤZ|N5k0Ϫ�e��k��k��
�1 wxg�|���c� W�I3���P5���hg�M��D,Z�5�!�=d8d�?�;e����&���Ѳ�a-_�qꓣ�J�����y�{�퓣�N)�~�2�<n��䚜O��]̪��^;�0�DU��}2�6���}}X�>�d��t�����h	����NPol��w
p�/P����i�C��h]m
/%�i�b	\�pg���5μ-7z�4�g��3��K
����F��'���4`��F��Pb}q	l�&Z����VJ��.0 �p��b`k4dy<kBN�z�
2��P��Z�r����'z%r�hf��ɇr�M�.�c@&�����������]�>r0yFF���7!���";c�X"����������$)��:�M@/' ��r��\Ґ�M��Z��ڂ���z9Gd �}dp�;���4de
����4��I�t�������5: ;>6!�ѐ�9�N�+���7�qO\t���S��b��~(����ñ���r�GB_K�<#e��� I����k�ה�3RLn�Xj�/�zW��v?����],&      �	   �
  x��Y]o��}�~ž߈����[�MѦ
���"/�M�Ddʠ��鯿g��/HqQ�fE��̙33K���LI�[�$������I��V�٢���yT>��(����'Rm�GJHY����/�){�Z�?EZ��^����2�eٛ������Y=C�
R�R1?���XX�Iy
.�T�nKfȼdp��g�����,pZ�8m���u�v��*ؘp�ΰ�r��<��1Ng�3�2H�2����H�*�.��%�l�01'�N�$�&�`�Ro�N�n6Y��v��|j��P��f���?���oU�0*��A�0Pp�jkr��y��1F�e.k�M�e�_�Z�� �!��
�r�(�	y�U�E��Hl���]��_��|�LY
��]ڪiNq��gA��A�Q؂�Y�6V�σu�� ����� 9U.eTڧ��w+�
��&_gƕ�Β/�LȢ�d��c����[�,���䔞3E2B��2���F%��)��2asg��L�YOB(4��C�X��H�f �*�
�ғ��tB���{�kf��Xur؝�?U� qww������O���+�+�Ϸe[��^��]��'š��/Uy��O����a��:wZ��Mh6�������D8��3��9�z�[���?�����ZU����H�����,1Yp&k���qL�LH��L��!U��V�I��Qk�?�';ҧ���7�P�@
��~l���������R5Ƕ�*f��a���	�Id|�@�%I�q���PJ�mJ��S�_5Sv�Gq܋��n_ދ��X2�
��\˧��ĿDyW=cc�����<V���w����涪�P�սxطHp�?������������������HϪ������"/��X�O���̓@Y.3Z��Vv��*y5�u��2CԜ!���)�;!��[#���@0���A�Ј U�� PΏˌLz�9WP���sLX�� ����0��	u�
z��������E�J��]}W�*�?��L���%�s�J���UK����7]u�`/����3/�u���~����+��;�dX�:3�Z��Ո����Z���PN�n-�������^|���C���z.��P�� .x2z)m�s�b�/�\%ś��3�q�.Po�����~����,"U��~w/ �l���G��꿹@r|��vS�Umuۖ���į��:TH��iw<dW%��V�TGB��-WZ�Q�����+:��ȏ�Sò���lz��c߿0���r�º&��"�3��ʁZ�gQR���*pW筍D�tC�!�>���>��X�_���<��I�������e\�^I������HY�A��&�+r��'p�I�&��9�b��^������a燙6j��h�\QNǳW�U��/��h�f�v�7��;񶭛�ӱ7{&�y��yˉ��� ��Q+���K�-�^g�.bFՇ���Ԗ��\���]��A��=�t}�>���O��>��� �?��m},wF��լAo��èεh��Y�0+�XY��F%)�>�ksz��Zt�Z�m):K+���PB�8<C�柟����ǟC�a8pv��"N�DIǅ����å��6��;,,j�g���P�0��4#�iF9����uK:��ٍ	��y%��������w�}�`P�c4��tY|r�lur&w��8�Ю3p�UzAmý8OR��yj9#s<�J�(V7����I�=�O�;5�7��)7|�Y˫���O��Ѯt3��0{��O9�3���=�6�T �d6߱�|��x�ʩ�]R��Fu$Z�q'�j77��_�9�B��@��8+ӚM�1�at��ד�r��-���r����.Ҍ�U�0�עc�@m�j�����tN��wa�ق���3"�@d�ie�[�_n�P1rrt���2`��!\�����Qo�gQ�Yе`�%5:��\���2�b����2$����3��Y������@������O]��~�gO�Q�htY;٤�0*'�\~��A@Ҿ���@��zv��fF�a#�/�'̚��J��.2<d��tdgs�� .�;���_I����{$��.����_���Eldg!L���0���6ܴX'�9��!�O�Q��|	�Ya�P���X��{&��(9+&�7x�Qy�VJ;��f9'>�4�;8�s�є����ټ<��o;��l���m�fz^�y5������'y�6�,�Ӽ�Жջ]��e8C33h���I�pV���JiM�ۆW4�����4��]�w3~wĹ̓�)�A���l����=�%�#�t�&��ۣ�����/��܂��;�Zz�"a�@�^t�KҞL�X��ߙ_���;�cޓqc'�T ��3ћ�p����C1"d-��2���\0s�{���kƕV��W(E52���K3��V�q\��z���Ϭ:z�8rڂ\kfʮ~��Iuw�����-G����-���='���(c�AԸ�ǌ����۩sG5��I��ht �\�9�hL*�^>Pj��r!�h"5�Eh��;M�gQ��J]�yZ��~{��ꗹk��;\�'hI���ub�^+JG�̬��{Fw�$�򰸯�Sm.�ur���3U��%��ѹ��2���~gR]}�{.�J<$.����}9�=�Ky��;d�C��!
��Im�M[U�Ƕ�ʇ����Øޟ�g��Ʀ=�ùng��u�g���xw�����d��G>H'Q9S��*`t�&��n�<�nD���[q{:�G�� ʶ�Yv���|���A̡�      �	   x  x��Yێ�F}�|E��XL�/�S�����Al8��/��H��<�|���&%) A�h�duuթS�ZB�_H.����L��+�3��j��yUr&�ʄ�Й��iI�Z.���h�����7_����e������m�ǲ���V��㮣/�-����ɫ����'�j�w���n���ݶ�+����o�=��>�->���wB���N��A�J���V;��LI��LY����U��jexƹ1a0u_we]���}����w�oث�&c�l��1���h���*�t�]S�5_)������LLW�+,�_c�������NW��4���,WF߲u^<�2wک���K%(ʭ�ͼ�j�aU��T�u�*O��Bp���i�'��B�L)��M�)J:2�W.Y�ckffMk��!�||��jX�)���ͅ�9;1�W��@��.��9���̤�"�1n������Dhx,�\��I`Ҭ���k1)L·�-˖SV�-D���{��l��g�W���}ylYy�VV]Q��,�W�C�/�cQl���|=���R��k�S�����ÜG���	[�ߎy�����@�-"�oE�X�^F�F��+2�����s�WU�g���.�Z�}]�kOݩ)�la�cy���Lp�C$�Rξ�3*���X)�)ml�0��4	1�&bwb�YI �eA��3`� ��McA{ŘYq�q%��ckD�NΉ�gP�B�ϩ-5!a-�f�"ѦVT)/�����:�Sc�����-(E�u��tv�
�$�Tj�*Ó9#`��$�gT��I�\��u=�MV�!k^i;���Dy��Ԣ�� jκ�P�uVO�QPkFP ��J�!h'>KX��Zu�.���o"<�=HЩp%ڨM����]�Թ�p��)x,��bnxG줵<���1S(`oK�⃝�����,x��ܹ3I*�9%A�Scr�Q�2�2he��i�7)�>O\�$.1'�&mH��hs����l��^��d䲇P�ԧ�}��������-��۶���T�뺩�v{:Ͷ\��Q_��б�� �Q�h�ږ�v3띕r���� ��ŏ���ؿ�=v\�P��vx��;Z����Z�������&��M�ho��r#[x1�I�%S�8����.g��Qt]�~�>��1�/�M}(���PT��Ò�������{�òا�c�쑮�f�z�?���q�W�6���r��uG�C"��i��O�^f���=�%-�<��Q�P�5D�B'�
'ƥjo������$d�1�Ϭ�+���U]�[Q^j�4C���`n�4P���r�}?D�Qlsܤ��k�b��Q-�i�G��C��PrզD���B5��k��<t�(��g�1��P{%x/��x�i�������쒐����
� ~>��%	�~��Bٹ5j*&"�4pE�Z�q�"$8��4yN~�)V}�zD�dL)�Z9.f�8��D�B+�_"5�r��F�|7t<�BӰ�w�Q�0;�C�(�މ3ɸq��I�J�g�/����ZRe�5�Ok���"�j/�ƫ6b�g�4[�M-��j�k�A�D�����rS�} i�$f�=I��C ET�8��ٷ�m?L�hiВ7�^*�d�"v/1�%��o #1�l�y�&�����6�;��:�ɟE�5���0��`���#�!W J���H�s�9��5{��kz������䐡AW�m��b[V%]^�3���'gT1�HR� �Sx�UR�4���M��\f\x/�3;��w��d{srlN��af�E㍟]pRؘ�5�=�^����M,Y��C;�
MMۛK��Ǻ���!N�`�<6�'D����'�Q*�4��r�-|��>�M�����؟֘�����U�9�!�^E�!���o�Ӯ\�X/ZlU9���� v옳�5��c����>6Et�j:7���|��-���6u��;�χ��-�1V�)�eОn)�M5���B\x�~�� ^<� ��b��)o�7�-��}q4gO��-�`�Vw	OS@�l�Ι�S�6cÝ�o�R���)	'څ)�TP�k���d�ў�x(�����JFu+�o�'�=B�ԧ�������5�w�������!������=AU�8�&�rȳx?'��0I�oԡ\0N�y��@@�
d+)���s�>�|O0���j�=�uBņ�q�bz~���e8�/�s�-�����+�/H#��6�/�lr��p��k7L�����O�r��-]|BG���J�Ƒ���wp�ks�u�,(�}4�]���g��hYJ�eyC�騲6Eq����gD|�\�,���zC��5�Y.��Wwb���>Z}�7gSCt$���@�tO�A�~�L�(_jbny"��� ������J}j�2l���`R�M��9��3ۀ"]�� F��EI��(�\�-{�>c�!�����#(��%��a�,����b7����!����nR7���@Ehat��;k���J��J���+P� �5f5�%2L��ܻ���pܗ�sj�4_wU �n �+��C��eG�8�9� &gԯ�Ϭ0v����QԮ��|v�p�P7E��K��|@J�	�M����u��eՙny�d�Fpg�m��A	��.����|�>���ߤ4��i��u,��2^�!��D�1���!s�H�(O&��$	'��Nӳ��1���GB2�{��7)��Q��ff/�/El��pgz�a�2��>�ЍK����}z�!��#���_@�^ŷ?��\���(�E�AϚ஝2�!��#A
�����X}�n����=r7"�wU���0]=�H�	��T�h\�@%*X��xJX���G��g���}�a�>��d�4xŋZ��QV_�ª&I�)���r�U
-�D߶l�rꉒA=��#��u�:�>t�*@�é]��
��h��e����� i����?���8���hߤv	0����H����Dw9��K������>Ėp+�ײ����8p��\��|ZU�
���jiz1����kaE�:��bV����>������$��@Q��d��Z�dU@�"�Z�UIpBw����`f݁8G���� !���`��~h������wWLa>2��6T��m0�`J�La�c;��7�m)MR@`��r�����h�T�m��~�qw������[�      �	   x   x���1�@��|�Nkc_�{4Ht�8��&�'�(��Ռfe�A O�c����Ō�^M��װ������Zg/cQ{j��B�!�5�\��=����lÁ ��"�ܟ���t�D��w3�      �	   Z   x�E��� C�e���K���Dz���@���,4���F���F�-}4�t{���5&[1�X?���A٘K�(�Yd�!�ۉs���\"�N�Q      �	   B   x�=���@�7a�^�9�׎ێĔ�<����A�jE��="�h��GZR�����      �	   2   x�34���210���L�/��M,*�21������M-)�L.����� ��      �	   d   x�M�� !Eѵ3��2��1����sI`nk(�3� �kV/k9�<�yl�F`X��l`ǵ�kX9��}���zn��T���0���7ާ���1%      �	   4   x�ɹ 0����0Ov��s7jDm�����n1�6n����; >j�
�      �	   &   x�342�210�21b3.S mf�eba����� \�3      �	   �  x��Y�r��]C_�UYD�"1x�*�$K��\.S��)o�@��4 ��o���%9�/����*S[��}�s�m�ǲ�9�x�vc׋��Y�r0�Y�����-��NlY�鶩a�p�0�n�l�t��'�O�hX��g�=��4+֌��"e�Y*ʧ��K�����Y����ٲM�紖�-w<��>�o��`"��0+��E���:�ʄYێ� �3'r�� S ����v����0����o�q��g^���w��/�{�kz�d��o��d��Ϣ�r�g[�K239<���[�܆���)}۱�Qd[��_>�z��Ŗgzvhu�Xn���);=eu�?�ܟ;a?�6B���`,EC�y*�zbIrxL�E��r�	v��!g:�lD]��=M��dIZ{K�v��T������=��X�-g����&r�4u�
Ɍ�[u�O�kz���#贡�̍�0v"3����G]�����X��+M~����b�j{��:��zx�|v^�7��yk!�;���y��IS�lt��Ƕ�g+��b-���ɗ�ؓ�\�w�}��<�[9cK��3�]���rS@����d*?���T�Xgޛ���/���me��4�ݗ�W�=Kۚ�l�r2���݋���J6�!_x��ػ���L�q��&{W4������	�7I��>���$}g>�-�ȃ�Y&d�C{�8;��!�8/��F��g���ɞ�F%����J�l�%��mV��TD�5_��f�l�ZI:��_&�(���r�5�{(�n����G�F��E�m�JV���U����HX�.}�`;!��
[y!h���Ah50��ȉ��(��E�Z�$aD]p|,0�(� S��M)$c�h�={BV�{L�=�7���de�s�+�}��d��c/�qux��{�������=
|�F ����%{�E�s��b��a/��b[�ĶgF���#7��E��뇮5������=�����0����Y���b+�D*xN�+Q�L�-�%JXc�{��8�#��Ӝ���ey��>Hk��e�V�L�ߥ�t��
����W���a����C���R
��T^���

i�(,�sR�,�R;w��j��A�>R���(�?86�;�| -��P�7F@�a�w�S�%��d]B��Qs���k��{žC�[�H��u\?g'[f����'Kp�b��q*�l 6{a�����;=P�g�$���q���6���c=�����&sp eى��� �&��#[�9�<��AW��:�UBz�aW�7l]r�?�W<���N�R6�5j�}o�~@�U�4)�-�L܂�s��[ӽ��X�*=L��,pz6�p������/�p���Gv��s�N��u���m)r��;����Y�Q�D R��kA���$8Q�g)ri��X���N7k}Bϻ\c�(
���*D<`U�d���ha���U�����A?�A���q� ���݄�a9�=[��"<�u��G}*a�K��?����v�ȕ���R����NY�Jxj�D�m8��N�j׀O�Jfu�02���*S��0��8J4}���F�(ߠz{pA�)a��?a~���� %+}��M�~q$�u*�kš?�:�wd0�l�;t�r* α��4:Ng;ߙ ���i�7�ao�G��*	���`���0W��B^(k��W���B�T�_l��6i:{B�̆c�����ń�R�d��R�����TF� �<�N��G�^���T�3V!ɖr��j:�D�J�g�����T�ե�f�[�,"���J��4>�� ��{tl4�R��k�y'F;���%VQ#,��1�	KHS�/nJ$^1�ag��7�҅i��C9����{ɨNUF(`�����{	��q(�g(e�{z��j�ӆ�zN���=�ت����"Q.u�J����9����(G�+�������e�"�b�d �&s"+F��(�=��7�^�"���.�<g���oc��sQ�ٺVz�����r�<�{'P���I�M����+��Ax�qf��9h��0B��p�����6��{�E���a��K���᷈�v2D~x�jOe��kg��3V��k!��O���,�-��R!�ӈ��[�kV�$ԯ+�*˂��>%��h�mAb�j��ɿ�	]W�.�;+|�� �U��%RDI�'?*�I�ȓ��ـk� �i���K� ��&�K����ܟQ�|D���g8O�n	bmE��EW,g�矈�$"V�1"��k��7����{�[D��/ޮp2����ۈ�w=2?�d���>�g������ʨ ,$;w�*��Nx�Z찉��+ۚ\;>�e^��,@��Ds���}�"X�W��g�m[��)�[���U3�j9���暭E��ME��t�����y�U�����S��߰C��u�Fa�`���|eƞ�L.�u��!�#�R$],�c�ŏ.8[����XD��X��,��k�ڪ�k��t�:���6)�S��by� P�vt� @⿻��t� 4_"�����,M�h[�
'�"W%�If	�R ~�U��(
�ߥ�Χ�����W���V�ԧ0;f7�t
��Oͱ���ɚO�/-r�E��8ț�y� �[t��A�dͫ-bv�2�[���E���ޒ�0Y��Y�ݲ�$��LV�~���#���E��w�ޔ1�,�2��M�����A~#݇����f4�ڳ��vbɣ�Q6Y������B	� ��m��U��"���Wdz	qtBk�EX���Z-�\��������k�l��6$(`�BJQq���� .jLL���JoI�<]3�s*q
N��=m����(��H(]S�S�����@J uPG�C��ԇ�������Z+d/0*V��"��t�Cע�h5���D����;��1���:*TnJBB�Bd(�ܻ�b�d8%�Q$�A��h������PU�ڊ�S��B�ۿ�p�}Z��K@�ﲕ�n���>(P��T���t[�;��8D)��w��&��R��@�bhʭV�x�������T�u�{'���3\�I�D�j����3>�*ժ�9Bbg��X����SU/�[>���n�:�ȶ��V͓u]����Ծ�5�y�Ovv����.L��joV"��� �$�衆�����Y�8-�Z�(
T�)$�V����Y�t������-� �u�E��m}�������~H�_d[Nг�7f��y�;�Z_Z��A�g�̳���Z��      �	     x��V�R�6}V�B@����4\��0ex1�N�G�����e'$����L2�hY{�}��b%�Sj��+1���4�2&����@�D����y�	>wa�yt���j���x\-�YȚ���Ǫ*���O��)����Y#���ɬ���_�EA�t5`z��ڔ�Tj�Z��;�����-����B7����R5d�����*㼳�)��-Ws_�I��Q�z��ȫ2+�o��~���S�b*57F۝�d�f*UI*)Q�	Ӆ"�x��)�ç?de�NV?�~���d]f~����W>+�]^8�;|V���]D'�Ë��~�GT�}�����Hv4�ƌ�4�$Fj�>�è�� ��Qy}}��WtSyGJ!��\
K,�B��X�O�0�t~z��2?s�9��h�gS�(r<v�q�>�G�lX�Ѣ��i�@g+�o8�|�T�5�@
e�e�^���������2�q�\Uݭ��㇢,�lQ�g�+��T�?]��[o��M�N� ��R������pl���h�+F�iS*	�TZs�n���+pf��_���ja�v}T+4��ݺ��u1�Lo��)�}RXz�j�����!,�-8�vՍ�8��O��^Wa9o��e���|�X/)�a4Ѳ��#�-e�$��X��?d���:g�B�GЮ��-Z�>Ұ�g��j��bV�=�T�sK��"�b7h۵G��8�_G#���3��h������i��Xf��ӧ���o�F|����o�R|�V�5̙����X}�M���G�8�o���,��yd��^��2E�J4��]���q�UP��������x�Gט�]mX�>MRe��*����a��j󕒀Gթ
Ȫr��<p�)9�ۛ�g�I���NT��&k05�)�F�$�lg��Pc��svzz�� x��C�ZZ�P0�ㄎ=�{����M�7o:|�7�Ӿ�¨M���zw��5�0q)/�V������,깛bػ��P,�� �m�<��V%�Xm�؄%�x?A���e/��xO�6Θxm�&�V���	��-Ɓ|�֞�`0�,��      �	   �  x��X�r�8}��5�fи�o��K��Iv�djf���XH(RE�v��� e]Hړ��.�t�i�� A,ጹ��#)�\�\�́4�O�Թ��9�&+H��u�M6B^r�����K���.�vC�bA)����Y��WeS�E�7�T�Pݧ~������:�qʆ���3C��Je.��d�;U�[
��Վ)שԨ�����b���$vj- �<Z7@șʙ˄��`�|W���86c�^���1���L:f��#��|y���p�̘�l$��J��3ƹ�,称�U�3�q���W`��f�`�ex�M�4�|y�@]
쌩3p]tA�XƔ�J���̙̕�$�{W A�Ɠu�C������赯WJf��x�coM�1�z��i�f��|M4�$�p �r���K�?�ĜAw'��2c��;��h�\Ć!m���J$�D���M����}��ulW3��|5	?�(R2l��oa�̸i�<�ie�|F�1F���P
&�A�e�=��;�}Yl)�:�1sbyG7��*�ת�Sy')�?Ҵ�##*�Vk8��+�9י�,�|��]@���D�� Ⱥ�n�m�/�۸y1ߖ�<���h7t����m�q�uՖ��*'���ח�3�S^H�K�n, ��=eU� #�ʈGQR8:���>���OW~h�>�U�E|K��Ô�JZ&Nا�)D?�a�c�";�����KלJ�ʘ�X`�1���E>����m��~����e��M�@���Pob�%3��dK0�f�� X;�7��1܇� �)B����]B=o��|[��wrL�R�r�87A�T�YL�>�̐K̋��[�$�׾�/��^�9u��O�@�By�,s��6_�� X&9pe&HL-fu_�;煟���W�~�Ɨt^Wؕ�Fd�S!�T<'��	�Y���c�v���W!��F�50�Y��m"���:�n���3�S��`�z��;s�)f�u�8����U��*�GOa�jE������]V�&��W��]�zq��K��}w��vL�vBȧi�=�y;���yV����k�����5���0���,K޴���+���c1�j{�뱔��;*v= �j
���yª9^�M�C���R�&K$�{
����SX)'.qh�x>��z��&����c9L�X;��³4|pM	ɥI�1-�هF�M]�0it��EKqQ��5��&���LǦ�bh������ǫW77\�X��?`*�����Ʌ��j;C�Ǝ$��t-F6��w^�o��^ӿ�*���0�)L��f��M+J&P �J�V�ҍ_�Y�;�(\��W���ϵ�cСU;<��,���v�����S=�&7��>v1�f�S������!F�%R1��Ŷ�U(��,⼛
��zVmM/p���`@q �nع�Ǝ�s1��c	R�)
�3g��;[;��8�#z�E�X�
Ӗ����ڱ|���X����(�pNŸ�Wj�ckPm]lw�� ��K!��l���j����{�����oG�ǈ����o��Ԩ����p�M(Î��]��n����u���囹��.SO��K[O!s����0���u��kpF�����;H��2�r�[5���C$���ny[m��Ԃ�q���k��=<o�8^��	|��Ǧ���Ik��[(���cx\��Ġ'�Ol�M�q3o��L3�1ު�pٳ��=���ߧ�@�~�,�8��CDakL�J�����
կ�E��7��{�DW��)�����;
ȥ@g�c����*s�2g��łųzU�XW���w�Α��֟�,.�L���+�eX%́�)�Ii|�擄{�nƨ��_�%&PV��m�*��z
��]��TI1���0㎩�|D�]=^��J�
�!�d�'��H��g�4av���[-{|�Wk�G�ia���!=�Y���3VD��eD�T2�'��h�d��쿛��z      �	   �  x��VM��&=ï�-'� ��m&��0�;�;�!���MVZ���ߧ��G�lRv��~��8�#Dm��P�Z��;K()3V�抲BD�gS��`�O!y�Ƅ�7O�a��h{���,�#9����&����"O�S�#�uI����h������;�sHQ
�J�(��\Ӹ6i�o\0=��um�����]UG��M��s�2+ҜЂ�[vk��'��{}�����=lzmk�K���RS�<��)��J� �4�R�<���9t^����>z�D�����	��qr�J�h!������.�����4@��Vo�k�	(�Pl�!�X/\���'�����JL����a�'�w��^�~D0%Kʬd$-rRd+�o�_�PLp��2c4��hm�|�)]҈��TfTfb�g�ޛ��M�c�L������p��`��ؠ`s�+�V�ޠ��چd�z�t�+���=T���Ċ�4[2�%�c9/��z�]�c�#y4�=<�k/���-P�`���Ɣ/鋒d)+� r�~���
>�~��>�eZ�\��l�X�1��ҙ�.*��Z{^	�}�n��W�|I.KNSRP�����ݙ�;�)?Z���F�]{]�BL�%�*3
9q��
�=uK�����m���1�>�'��/�g�^��&eL@E�C��M�����\8{0��	�MF�}D@ATZHE�+}y���[ۣ����I\��Ɠ�yJ�2�/�.��D�Ȍp�9����_.Q��:�6J�7�n�����Z�~�����l�4�;XI����s�36���zP�/p� E���9�����'�)A>l����W��Wޠǡ�-��5�P���l��+�kk��Qs/�{we_i�������<�Rr�W�fh�%�z1���ހ��_@���{�L,yಅ�`�e�??B
�H���I�ј�|-:/ ��|-�Z�Gxh݌������`[���"bł����Ȕ�ْa�6�W�X�w�	�ێGo��k��c�/�̦f      �	      x��]ms�F��L�
|L�,h�_�uu%;^[�rV'����ܩh
�p�H-A����� �`f����u�F�<==�6=j�H��䈘#J2jN�<!6'�J%�����1�QqB�	%��F
���f�ˏ#
_#�FMF�	!���eJݳ��7���t�F��l>+�/�?���jQT��,��}*&��uv6���|1�/���ru�xE�q��C�(���}\UU�gW0��!���划WT� �:��n5�1TnNˍ��
U� ���=��\�><L��k���>�Z�F�O��G���5�����켸Yfc�wY��-��w���u��rQ-�O�2��d? �Ͱ-�PK��I5l��S�` P1�Qv"4`�甈�O�'���*bLM����U_������󇬜]��񲨲�b�}W�S��j5���>���}6�,��
�_�&��iQ�YǤ����B�W��8�x5�M��O}hӛyK�<����ݻ2���qUdU1-�'�gLzUL��Z$�	DB����+c��Db#�R�\a(�%��P��� �����;�:�p�����:��?L�Y��b1+�U}�/C�@��3��yj��Y9[�%�[=��i����W��HW0�jrb8a:�+,�\sn@x���,./>i ׋�^G��~>�.�)k�04V��D�\)b�H�F.rc����R�o?�A��o�*�Xeoǳ��QK��:=�b=	�y.���&��E-�(7J�zp��Ø9�>��r=��vШ��X�z�t7�	Ok�&e���ꕸz��A�(�|��P�	���B(�"*hOk��H���>��g��3�>-�І况��N��ߞ7�^¡4'��̍�L��L��rN��ܓi��L�_�!�r=���J@�ٞ��g-�`�
��<F,�	S�0�ja�0�#*<��x�(��4�Aq�M�[�8�~�Z�[�ؚ5���w(˅�D��<M���5,0�4�K����.׿بz�ϖ�Y1_U`�K0�_���o%xy����0_�f_�g_yҮ������gw��F�!��e0�>�Kℙ�2��q
��E�$��8mo1�x
.X�����}�M���1{(�߳�+���
�|�t��Rܖ3�ͷ#����ivS\g�^L�u��ć�Rr3_L��*�znT�\�A�_��i}k5�,ʛ�����Y5����s� C�g��3�����%��s�c����E�9�>�h����:W�iV{FJ��`-*-:�Z<񀫵���Ad'��FT�F�qу��Τ��T�6� ��$��k.ï�|:�9�����y��.K\�U��U19�$`���T���E����D��࣪\0�h�Hu3�)*���ϧ�2G�������M1�E��鴜�r�wg�焾C{Ӣ����h�>�}|�m#,B.�n
רJ@��b�T�	]z��
�=<��<�6��|M;�-�32�=������� ;��x�
t���r�|LuK�}�%JM�c�[��ù5&�V��$\j��nU��ޭ�8* �z�U��g����)���`�X¢�ā���ڹ����u����s��^`1D3׏���i��n��`Oo�s0�,�tz4-�9Z��e�m0�`y��c��ߍ��=�:�_3�g<�*�v��IV�V,���~#������������ۚ������q[xܖ�#��w�A�� ڐrjXB��ӕ�e�J_��^���������`�uf]��}Y(m ��T���ϗ��s�7�q�y[5m��Y�� *?3��z�)�b�Z�|Ŕ��y�9�S�L�F-Yk����
��eg48��qY���f�͢�����Z�����e6`��@B8>���u�&���B���+m�M%fz�T�����k!	�]$�{�b��>����5`Xl��	����Tt/O��5���{�����֎n4k����c��(CY�:�5\�^�N��w�V=�w��oR�ki�$Ј
�`�_P���"9a֢	�
Wx��z
:hk������q/-���V����%b��p���p�Q��ߡ5�r�l��n�0��I����In�t�P�C-�B����!�s�q����FVfqߢG�v�X̗�����-����JH�r�z	�PE(@E�x�
A�5!L�|N�զ;8�Mg�t"R\qv|a���s�784�	�%&x.,���h˘]s���^&7O���tj������4J��Fp*R�qk��d��m��aj̚�r=K;Y���J@�4��u$�������H"{��4����n�9z��Y�tF��v�������brRh�(nk�Oӥ���1{������΀Y�2��鲷���pV�r9a"�J�[���=j/ݳ[`����u�z����)\p��0�������yk�`��[s¿��l{����a���tZ���Ӈ������ϯ��Y�y���n���_�՗b��|�ܜ���#>��_��`���c1����x�=,���eYo�`~��VUq��(�p�X�|�.�~���Zb��|�ݬf��#�N���x��e�Z��N����1��o3�{�����>���f��(� \�E���Q�P)�祲��gl�wpc8�A�x�eE1��`�����}w;՟��ak14QbOW3$L?��$bZ����GL�BX_����X;;��tA"�x�N"9���
�'����<�g��k&t��E����
a�N]v�,7�?�LwLx�L{�4��'�3-h��5�(����3�1�*'
�KZ����Z�w����6��9�TuZO��'H�P�E\��?A�mx��3p �z�Do���I_(��<�m�a��)����;|Q�P�P��*�_�L��_�'[R�]�C/=��ܳ��<v!�*���ڰ@�-�\J{�T)�3v�6��]���=A&���Bh�j.��ώ�9�Mz�����`�hи_�u�(�Ƽ�M,�&[v��/\�b�� ��ޜ��hSPݗ�����@���o!6�h�DfR�q@m���
��f�e�)/���q�>ˀ���+z��ܴ5�~U8����d}��l-%�t�W�z�/��2��xv����������ϧ����Ka�G��^��>$�A��G��c�#�.a�����-G�h�"�K먫�Lب8m���7�[�,|����]f.���+|(oG��r��hZ������g3��3��X8pL��3�E �asg��Q̶�C���t8��m�uOx���8�F;iXd� �����:4pݘ䊘u��z;i������M4?ȷ��	�	t傩(�S�0��o�_ze���9��`?�,��X8W��\�U7�oas%�a�븁�q�f��'��� ���3N�o��	3��U(�hCN���#�,b��N�&�_�]SR�55���v��;�0��a`re臉��F���@�нB�}v�Ο��]��Y'�:�L��`D��
ʢ�&�6�{q����5�9��r��E��&�Y��B����9��X\�0F�4zLm6sz�6[o椒��J���1b��M�q) �w`C��H=�6�z�����s���S�#/Zh���@+�	�aF�B���D�m]֮�<�:�gá�s��O� �c��Kb�L�PHm�"������;{,�d��NA"�����5JhG�&��{�!����!
��g�zх�Ӕx�b�Oib=��Fr�^���z�L��=9�/h�c�^�P<u��qԅ{9@�`��4ޏ��6�b��n޾�9c��Ѝ78c�`�T��<+�6e� �X&��
��]����z"r�m�]����T�(R��5�muJ���^9�?b�����9��=0�ߝ�,�p��y��מ��L��zIL�fL�T��v&�H�����q}a�8 VA��	1u�������.�G6���G<���?֧��nAx"~4�\[�J�C(}�l�pϬS<'-�����3J@���swbVX	Z�:)]���x4����cQ�Ӳ��g�>'���˒���b0�`�Mbn����D��70#�لJ�[    �0����;��lv[T����f���y��>fS�I��o���[��FX�Ep��-�Ei�k����S6�Ct�{G5멥��c�C1!�C��}�z�|��<��c�I>v=Ѭ2\�Tw���� Ԇ��T�s�u��E����߰���W�qg���o�'Ǹ�G5�֨<�}�q~|F�Fir��\+��ؼF���"Y�?���vaiּn`�V�w�n	�/2��"��"#*%���X��mN�+��4'F��ZV��� ��aol���0TsI���m�b�c��vǁܩ���xZ�M9-�M�����G��Uƹ��e4z�-��*�a~�Kcx���ヅ_���`�$��B���:�UA���dj�$跱[���18���t� B�⧼��:/e���D��Nk����Ms��o�m��Q�Ԉ��P�[�%j���x�-��Zg����:э�[��`Tģ�-SL�x�!ՍwK��7�/�v��YMp����)t���F�#���=�r�P����b)���
��L�?e��On��67n�����3��7��펠C�ĩRq/#�'�J���S1=@*H�@���R�H¿xN�p�J�5S���yX�ڸw�9�� 5�
l�B8��z������wb=	q��G�g�(�#�Ldb�Jf`c�i��e��4]�V���*�	�%���6vkZ��nm�ޣ52�T�1b��uf\0.��{�T7��Ly�H?Խx����4�T��طXN����kh�]A�&q}[Dt�������!���#�J؄�SݸŁ�}N<j�ղ�1�),�dJ$܇��'��·�-�C�Y�����=�9z�oV�٣s����_����U�i{\�&���t)+`94*3B�T%��J��F	��}g�s]0�IQ���p�
Kl��r����K����%�	o����>z��*��$̲���b޴v��:m�h�_����?�@��ϔJH��������,�gC��!j�>S�L����<��;�g�c�&o�y�c�J4�U��Ȗsдpe�[�X$�����%���r�Bs��-�����l>�ξ��캘���b�������6Cn�7���a鮳	��p�g?�A9?��dBy$DwY��O2�T� ���n�|����n��G�s����f��D��ah�vkh��~0�あ~����˪�\��(3�jRw	�~ako]�u�n�s�Tł;G9֐����l�^�8�ظ�iS�G�j���-���d�U�iy��ޯ3
[����X��/�E���}��(���cG���/���.��Pv n�1%A��Q�_��N���F9טJ1o�v�>Q]~�G�>�]�a�9��|C�7< �9����ژD)zLE�^k��A�em=Ld�����K�4<���7]�k�|o��Mo�O�ٟ��ȱ��kx�D�Y����f��=������v"m��6����3��˔xp���X���ٖ�=���
v����f��=-��.Xb�C*�>�SlT'A�k�X����;�>,�	n��S��O/e�{����G���4���B�'<d
}�氳o�}P���|���h���Ď"�:c*��)�]9�Y�����a�~´�>��͍b2v�cj#�'�W|�O��m������[�]BaQ�*�6���?[�S�>��\/��fM"�&"6�ա�*�-���^(�s'M+c������9��A�F��q'�+��p�:�=��~t㳌�V`Vp���-�����/B�O� �-e�$�$��;HֆѺ2�HF�˵��a�w�5�吤xA���
J�������юADD��ۿ;�M�!��7����M=t�1H|�D�"J&��<�|JA��~�0l=aD��S��_��l���F�/~�0l	>4"�ݹk�r)��QS����MÖ�#�@Ӏma��/�nإ�@d�I�T�6���UC�6�/��6����ث�栯��Q�N�+ըu���E9��鍪_167����@�T�K���8��V���[�7U��+Zy�7>"�V��Qmձ�;7R����4��r�[���k��p[WU�=���P{��y_Κ��0���n��>l<���(��v��oe��	W��ܶz���!���/�����)EΕ�6a~Cj��ԡ�xE$B�s�ʵ���R�9��ڀׇ/_ ���~�¦��֦6�bj��z�*Ϣ����eΉ45�[P
Bd�2����*���Խ
(�O	�׼����إP+bD�������e���lT�wIA��*7��T�~@m��Ct���z]R���x
�#����@�>�跃�yvW���Ԑ��RXX�m���w��Z�ή�r�Ϯ��A�+\�W�~�_����
`{h �+�a���:��ؙ��L�ŌY���F�/['���=�_�)��Sa�/*�TL�W�x���^�3�o����C�	���9�~��r�y��Y�w����u�(&8�7�&�ʾ����3�yW4�XW�N�HLl@u�>��E���5�b�X{�k����$�y�?8�A˶-�ж)�w/W�
�7?�6������������j>�6��^�Y���\)���Tj��SP�<.��̍�c�o�c�83ގ���	'6��\�_��r#cCS������5�hM���j<p��&"�R���؇��أmb�����ePIj�]�=���!?�B�x"��l����G(1�A�� qO�f:vͰ���k<�6������'B3�.�o���ʘ��'C*�E_�w�.�.o*:/'嬄�ˣ������SB�(��x�9!bF֧��q�S���&���qՂ ���<#>���v\�n�T�u^(�SnJHm@�o1Ӄ���LG�.z%�[��SJ�S�j�]g~!Z.��M��&� Dv��\w�}��r��Rb���#��Ey�	&�0ͧ��wc1~�4lzh��Ѩ��?���)F�wa����3X{/�[s��,��Z�z���A��C%��SG���'�9o+��ぇ���4��Q��g��/AE�^@HڹmY�9��aE�ZG�>AmX��f�%��)e�����1\�JmH�ϖ�6؈����ptI1@J�[�4l.��6��g��ؚ�	0,b�t����A�4�Zӫ�^���<T��vo��Zz*ߚ㡧,�!8p3G���)*�b%��rǂ��k=r���p-����p���SB�`�fpv�	�(���AE��D�@�Lp-�$�T�LԆ	��0aPl̈́P�Pڎ��`#s������
��`���:�̽���x�D>qLm$a�?)	LB8Oy[�A�-0�k��b����Ʉ���a��,x	u�rb�P��p�I��a��,x	e�rb�PbV7WJ�T�R�o�����X�V�^_����As0�BGRS����wJ;`A��v۳��}�?eX8?���Q��*�pӖ�������ɪc�&�ք<áC)ᑥ��?����c5O���~h��?Բh#�~�"#c�ҵ,R���Yr�96W��u;-̮-��ty�{�P��F��bK��@(+HE�J������P=�s�w�ThA�}��>��?�"4����c�W���vu�Zŭ]��(��5�ܷ;�`��S{{�f ]ܚ	��j ��1 !��W�0����?y�����8n,ꯐ���WH���[�{߲4Rǩ��ڰE}��i+��}��z\	�H7s�P�1�w�|����
���`b��&l�FrL�Q��dQo�$����!Y�j3&8�ͦp�i4ndHmֆ>���UW�}V��V'4	��M�J��
MP{���j�������b�{9��3y��W�x���z"A�
D�M@��T��Jecb��z@��m��Ј���`D%c�CLmV�9Ȋ8�Nw��C�6�
�[�w�P3�k*�e�lI�(}E�i6�2��Dl)8	�N�E(���륩�{y �  @���Hى�[pMB�ȹ�,�ST��ݶS2�]�J1(/]�j�^��:zJȄ�_p��!�Q�� ����AY0$۳ ��J�N�\���)9����/�+6,�p�O��m9��4t\�Ip���2�D�ߗ>^B������H,���[����*�;Ӈc�P��x�U���y����ǹ�%�󸮤����Ԃ����`�	8�����WTv:}O�W@q�|��_Q��+����p��^�/��/��%�W�KH��{�H}��nF�����@y�_��	he��a�TI�֛o>Z��T**�P������׈?/���[�����+@��·�8@k�&�a���7�QI@�cT½^�;��C�N��J7�@��&V��Ou� ���x��Ey[�}t���!��+��c|��bq?���(NS��8�̱I4��[�`��Ou���5 ��p~�K:�ߜ5����ƹz��ǽ�����O���S�O�| ��|�N_�S)�h#�!*e����G��;����U�e���Ǐ�{�M9�LW�ES���Z5{s<Q�,�6��{����p�"p7W𡨝p�~s3�]'g$����L������mV���eު����S�O����go.O?����j���xZbGX옋��G#���իW�{�V      �	     x���M��0���)r��)��]� ��4��@&�\��؞X�^�ɟH�Gc��Ҟ`�܂�	�9������۽����[���������S��l!��� �T /��ǡ��5
QS`�R>�����cr�JT�`\�|R��ׇc�3<YU��yUo�F�� �1�Q��U} M�s�M�=���g��/�B+�9E`��jq�����Ĺ��SKҢ'�
����?ݥ�?�E�~]���emx?���	�U!<�-֢����BfՇB�l�sRcϓ~�x�I��$�,�I�*>LJ3�C�m�̐U����O)G��)Ϙ�����0�u�V�K�p�;~<��Ah�tו��}_(a���ǻ�q������$��2�K�֙6��4���;]�����g'`����_�=���(G�Ś�<�� ݀���&e�:�S�VhYPOa�a�=��b��@���������4�h�����s����������j��)2 . 	D5�ǔ��J�Wry�P�C� 5P7\      �	   �  x����n�6�����D�pH��]�.z�^�h��֦�Bt��:o�!)���.�����i8��w��wB�M��M��I!�c���J�J�B[�z�^�B�z���������.L5>H����.m���j��/�fnÔP�Ҷ>=ߤh% E1E%J�P(�W������*�U��z+ߏ�1=ߐ�P8�(7,7)�;�͡��s3��Єv!��C�*-��P2��m�?�І�<����O�����=%�[��aS� E%e���%*i�i����5O� �Ц�����pu��m�?�_�e�11
+)
aP��g:��W?���o<d= !b`+銲Dg���� w�tl�1�oپ�����rJ�4$�|#���v��v�_��s��<����M�r��e��Ub�Y�RJE>'�N�\����\��lR��)P�4;?�ݷ����>AI{�@��%5��,
�Q@J��8�iZ�����:�����!Gj��Mv*����B9M.�Gj�����	AU)U �zش�3�����60��\Ccӂ�
���=�p`*��(kQ�a�B��d���Rk���p�8���I�������y�'�vȍ��L�rM�U���2�'�an�iGOFޙ4]�(.Q�rE�ԕ�m\��1��
�1!��6��q�H���JA�ԥh��9bcK�6_�B
ǟN��E�Ey�bK�@Rsէf"@��6��6��=.�5h�S��)��(i%�ܰ����u��Ě��.(t9��4��MG��g0�A�F��
�vi�";N�]�#�6��u�^��x��F'�L�<��4��'?��YmiT��e!��4h��,�?��K���жaO_QK�/������)%d��ż�_=5�PkN=>��!u�Ê�<�m�p����i	l��J0�y��D I�L`O��҄��~�<��}�5� �P��n�jH�� �M�+�jI+��b��R�!��#T����&�f�n宠�Veֳ�P���&��5�N��B�h.���u:����� S[�m+EB�e���8a��� �����*&��p�S�^�GW��D@,�T�LS�ѭޙ�z���}�^|K��/]��-T�$e�)��5��2�K��7��Ԗޖ�>ׄ���@�B�J�C`�)y;?����04���`�)L�t��Z����_>�qS�$Е2I�xJ�_�B,wZ[��sCK�B*i�tJo�/u��+�D��_̖S�ů�}s4��� MK\�Ckv�*�o�/
�eP(e>�f�)��Ʈ���&��F��Hbv�r���:F�a�n*����T�ɴ�(���O-��7rY(Q��0�Ӱ��o���[������F�o����>�t�I6����_1�� �J�2�v�j�5���EL���������9�-��\D6�6��Ю������������     