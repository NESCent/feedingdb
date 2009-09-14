--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

--
-- Name: plpgsql; Type: PROCEDURAL LANGUAGE; Schema: -; Owner: -
--

CREATE PROCEDURAL LANGUAGE plpgsql;


SET search_path = public, pg_catalog;

--
-- Name: pg_grant(text, text, text, text); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION pg_grant(usr text, prv text, ptrn text, nsp text) RETURNS integer
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


--
-- Name: FUNCTION pg_grant(usr text, prv text, ptrn text, nsp text); Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON FUNCTION pg_grant(usr text, prv text, ptrn text, nsp text) IS 'Grants privileges on database or schema objects in bulk. Parameters are the database user or role, 
 the privilege or (comma-separated) privileges to grant, the text pattern (for LIKE queries) to 
 match schema  objects by, and the name of the schema (public for the default public schema). 
 Returns the number of schema objects to which the privilege(s) were granted.';


--
-- Name: pg_owner(text, text, text, text); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION pg_owner(curr_owner text, new_owner text, ptrn text, nsp text) RETURNS integer
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


--
-- Name: FUNCTION pg_owner(curr_owner text, new_owner text, ptrn text, nsp text); Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON FUNCTION pg_owner(curr_owner text, new_owner text, ptrn text, nsp text) IS 'Changes the owner on database or schema objects in bulk. Parameters are the current database owner (or role), the new database owner (or role), 
 the text pattern (for LIKE queries) to match schema  objects by, and the name of the schema (public for the default public schema). 
 Returns the number of schema objects for which the owner was changed.';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE auth_group_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE auth_group_id_seq OWNED BY auth_group.id;


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('auth_group_id_seq', 2, true);


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE auth_group_permissions_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE auth_group_permissions_id_seq OWNED BY auth_group_permissions.id;


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('auth_group_permissions_id_seq', 192, true);


--
-- Name: auth_message; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE auth_message (
    id integer NOT NULL,
    user_id integer NOT NULL,
    message text NOT NULL
);


--
-- Name: auth_message_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE auth_message_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: auth_message_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE auth_message_id_seq OWNED BY auth_message.id;


--
-- Name: auth_message_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('auth_message_id_seq', 607, true);


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE auth_permission (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE auth_permission_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE auth_permission_id_seq OWNED BY auth_permission.id;


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('auth_permission_id_seq', 123, true);


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE auth_user (
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


--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE auth_user_groups_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE auth_user_groups_id_seq OWNED BY auth_user_groups.id;


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('auth_user_groups_id_seq', 24, true);


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE auth_user_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE auth_user_id_seq OWNED BY auth_user.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('auth_user_id_seq', 16, true);


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE auth_user_user_permissions_id_seq OWNED BY auth_user_user_permissions.id;


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('auth_user_user_permissions_id_seq', 1, false);


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE django_admin_log (
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


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE django_admin_log_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE django_admin_log_id_seq OWNED BY django_admin_log.id;


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('django_admin_log_id_seq', 610, true);


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE django_content_type (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE django_content_type_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE django_content_type_id_seq OWNED BY django_content_type.id;


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('django_content_type_id_seq', 42, true);


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


--
-- Name: django_site; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE django_site (
    id integer NOT NULL,
    domain character varying(100) NOT NULL,
    name character varying(50) NOT NULL
);


--
-- Name: django_site_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE django_site_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: django_site_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE django_site_id_seq OWNED BY django_site.id;


--
-- Name: django_site_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('django_site_id_seq', 1, true);


--
-- Name: feed_anteriorposterioraxis; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE feed_anteriorposterioraxis (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    label character varying(255) NOT NULL,
    controlled boolean NOT NULL,
    deprecated boolean NOT NULL
);


--
-- Name: feed_anteriorposterioraxis_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE feed_anteriorposterioraxis_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: feed_anteriorposterioraxis_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE feed_anteriorposterioraxis_id_seq OWNED BY feed_anteriorposterioraxis.id;


--
-- Name: feed_anteriorposterioraxis_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('feed_anteriorposterioraxis_id_seq', 3, true);


--
-- Name: feed_behavior; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE feed_behavior (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    label character varying(255) NOT NULL,
    controlled boolean NOT NULL,
    deprecated boolean NOT NULL
);


--
-- Name: feed_behavior_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE feed_behavior_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: feed_behavior_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE feed_behavior_id_seq OWNED BY feed_behavior.id;


--
-- Name: feed_behavior_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('feed_behavior_id_seq', 10, true);


--
-- Name: feed_channel; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE feed_channel (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    setup_id integer NOT NULL,
    name character varying(255) NOT NULL,
    rate integer NOT NULL,
    notes text
);


--
-- Name: feed_channel_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE feed_channel_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: feed_channel_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE feed_channel_id_seq OWNED BY feed_channel.id;


--
-- Name: feed_channel_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('feed_channel_id_seq', 85, true);


--
-- Name: feed_channellineup; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE feed_channellineup (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    session_id integer NOT NULL,
    channel_id integer NOT NULL,
    "position" integer NOT NULL
);


--
-- Name: feed_channellineup_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE feed_channellineup_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: feed_channellineup_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE feed_channellineup_id_seq OWNED BY feed_channellineup.id;


--
-- Name: feed_channellineup_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('feed_channellineup_id_seq', 65, true);


--
-- Name: feed_depthaxis; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE feed_depthaxis (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    label character varying(255) NOT NULL,
    controlled boolean NOT NULL,
    deprecated boolean NOT NULL
);


--
-- Name: feed_depthaxis_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE feed_depthaxis_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: feed_depthaxis_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE feed_depthaxis_id_seq OWNED BY feed_depthaxis.id;


--
-- Name: feed_depthaxis_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('feed_depthaxis_id_seq', 2, true);


--
-- Name: feed_developmentstage; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE feed_developmentstage (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    label character varying(255) NOT NULL,
    controlled boolean NOT NULL,
    deprecated boolean NOT NULL
);


--
-- Name: feed_developmentstage_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE feed_developmentstage_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: feed_developmentstage_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE feed_developmentstage_id_seq OWNED BY feed_developmentstage.id;


--
-- Name: feed_developmentstage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('feed_developmentstage_id_seq', 6, true);


--
-- Name: feed_dorsalventralaxis; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE feed_dorsalventralaxis (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    label character varying(255) NOT NULL,
    controlled boolean NOT NULL,
    deprecated boolean NOT NULL
);


--
-- Name: feed_dorsalventralaxis_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE feed_dorsalventralaxis_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: feed_dorsalventralaxis_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE feed_dorsalventralaxis_id_seq OWNED BY feed_dorsalventralaxis.id;


--
-- Name: feed_dorsalventralaxis_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('feed_dorsalventralaxis_id_seq', 2, true);


--
-- Name: feed_electrodetype; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE feed_electrodetype (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    label character varying(255) NOT NULL,
    controlled boolean NOT NULL,
    deprecated boolean NOT NULL
);


--
-- Name: feed_eletrodetype_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE feed_eletrodetype_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: feed_eletrodetype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE feed_eletrodetype_id_seq OWNED BY feed_electrodetype.id;


--
-- Name: feed_eletrodetype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('feed_eletrodetype_id_seq', 5, true);


--
-- Name: feed_emgchannel; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE feed_emgchannel (
    channel_ptr_id integer NOT NULL,
    sensor_id integer NOT NULL,
    emg_unit_id integer NOT NULL,
    emg_filtering_id integer NOT NULL,
    emg_amplification integer
);


--
-- Name: feed_emgelectrode; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE feed_emgelectrode (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    setup_id integer NOT NULL,
    name character varying(255) NOT NULL,
    notes text,
    muscle_id integer NOT NULL,
    side_id integer NOT NULL,
    axisdepth_id integer,
    axisap_id integer,
    axisdv_id integer,
    electrode_type_id integer,
    rate integer NOT NULL,
    emg_unit_id integer NOT NULL,
    emg_filtering_id integer NOT NULL,
    emg_amplification integer,
    channel_id integer,
    sensor_id integer
);


--
-- Name: feed_emgelectrode_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE feed_emgelectrode_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: feed_emgelectrode_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE feed_emgelectrode_id_seq OWNED BY feed_emgelectrode.id;


--
-- Name: feed_emgelectrode_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('feed_emgelectrode_id_seq', 82, true);


--
-- Name: feed_emgfiltering; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE feed_emgfiltering (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    label character varying(255) NOT NULL,
    controlled boolean NOT NULL,
    deprecated boolean NOT NULL
);


--
-- Name: feed_emgfiltering_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE feed_emgfiltering_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: feed_emgfiltering_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE feed_emgfiltering_id_seq OWNED BY feed_emgfiltering.id;


--
-- Name: feed_emgfiltering_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('feed_emgfiltering_id_seq', 4, true);


--
-- Name: feed_emgsensor; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE feed_emgsensor (
    sensor_ptr_id integer NOT NULL,
    muscle_id integer NOT NULL,
    side_id integer NOT NULL,
    axisdepth_id integer,
    axisap_id integer,
    axisdv_id integer,
    electrode_type_id integer
);


--
-- Name: feed_emgsetup; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE feed_emgsetup (
    setup_ptr_id integer NOT NULL,
    preamplifier character varying(255)
);


--
-- Name: feed_emgunit; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE feed_emgunit (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    label character varying(255) NOT NULL,
    controlled boolean NOT NULL,
    deprecated boolean NOT NULL
);


--
-- Name: feed_emgunit_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE feed_emgunit_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: feed_emgunit_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE feed_emgunit_id_seq OWNED BY feed_emgunit.id;


--
-- Name: feed_emgunit_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('feed_emgunit_id_seq', 3, true);


--
-- Name: feed_experiment; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE feed_experiment (
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
    description text NOT NULL,
    subj_devstage_id integer NOT NULL,
    subj_age numeric(19,5),
    subj_weight numeric(19,5),
    subj_tooth character varying(255),
    subject_notes text,
    impl_notes text,
    title character varying(255) DEFAULT 'new Experiment - edit this'::character varying NOT NULL
);


--
-- Name: feed_experiment_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE feed_experiment_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: feed_experiment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE feed_experiment_id_seq OWNED BY feed_experiment.id;


--
-- Name: feed_experiment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('feed_experiment_id_seq', 35, true);


--
-- Name: feed_illustration; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE feed_illustration (
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


--
-- Name: feed_illustration_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE feed_illustration_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: feed_illustration_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE feed_illustration_id_seq OWNED BY feed_illustration.id;


--
-- Name: feed_illustration_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('feed_illustration_id_seq', 4, true);


--
-- Name: feed_muscle; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE feed_muscle (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    label character varying(255) NOT NULL,
    controlled boolean NOT NULL,
    deprecated boolean NOT NULL
);


--
-- Name: feed_muscle_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE feed_muscle_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: feed_muscle_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE feed_muscle_id_seq OWNED BY feed_muscle.id;


--
-- Name: feed_muscle_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('feed_muscle_id_seq', 24, true);


--
-- Name: feed_restraint; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE feed_restraint (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    label character varying(255) NOT NULL,
    controlled boolean NOT NULL,
    deprecated boolean NOT NULL
);


--
-- Name: feed_restraint_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE feed_restraint_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: feed_restraint_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE feed_restraint_id_seq OWNED BY feed_restraint.id;


--
-- Name: feed_restraint_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('feed_restraint_id_seq', 9, true);


--
-- Name: feed_sensor; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE feed_sensor (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    setup_id integer NOT NULL,
    name character varying(255) NOT NULL,
    notes text
);


--
-- Name: feed_sensor_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE feed_sensor_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: feed_sensor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE feed_sensor_id_seq OWNED BY feed_sensor.id;


--
-- Name: feed_sensor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('feed_sensor_id_seq', 87, true);


--
-- Name: feed_session; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE feed_session (
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


--
-- Name: feed_session_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE feed_session_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: feed_session_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE feed_session_id_seq OWNED BY feed_session.id;


--
-- Name: feed_session_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('feed_session_id_seq', 33, true);


--
-- Name: feed_setup; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE feed_setup (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    experiment_id integer NOT NULL,
    technique_id integer NOT NULL,
    notes text
);


--
-- Name: feed_setup_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE feed_setup_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: feed_setup_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE feed_setup_id_seq OWNED BY feed_setup.id;


--
-- Name: feed_setup_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('feed_setup_id_seq', 61, true);


--
-- Name: feed_side; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE feed_side (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    label character varying(255) NOT NULL,
    controlled boolean NOT NULL,
    deprecated boolean NOT NULL
);


--
-- Name: feed_side_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE feed_side_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: feed_side_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE feed_side_id_seq OWNED BY feed_side.id;


--
-- Name: feed_side_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('feed_side_id_seq', 5, true);


--
-- Name: feed_sonochannel; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE feed_sonochannel (
    channel_ptr_id integer NOT NULL,
    sono_unit_id integer NOT NULL,
    crystal1_id integer NOT NULL,
    crystal2_id integer NOT NULL
);


--
-- Name: feed_sonosensor; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE feed_sonosensor (
    sensor_ptr_id integer NOT NULL,
    muscle_id integer NOT NULL,
    side_id integer NOT NULL,
    axisdepth_id integer,
    axisap_id integer,
    axisdv_id integer
);


--
-- Name: feed_sonosetup; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE feed_sonosetup (
    setup_ptr_id integer NOT NULL,
    sonomicrometer character varying(255)
);


--
-- Name: feed_sonounit; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE feed_sonounit (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    label character varying(255) NOT NULL,
    controlled boolean NOT NULL,
    deprecated boolean NOT NULL
);


--
-- Name: feed_sonounit_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE feed_sonounit_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: feed_sonounit_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE feed_sonounit_id_seq OWNED BY feed_sonounit.id;


--
-- Name: feed_sonounit_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('feed_sonounit_id_seq', 1, true);


--
-- Name: feed_study; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE feed_study (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    accession character varying(255),
    bookkeeping character varying(255),
    start timestamp with time zone,
    "end" timestamp with time zone,
    funding_agency character varying(255),
    approval_secured character varying(255),
    description text NOT NULL,
    title character varying(255) NOT NULL
);


--
-- Name: feed_study_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE feed_study_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: feed_study_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE feed_study_id_seq OWNED BY feed_study.id;


--
-- Name: feed_study_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('feed_study_id_seq', 15, true);


--
-- Name: feed_studyprivate; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE feed_studyprivate (
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


--
-- Name: feed_studyprivate_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE feed_studyprivate_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: feed_studyprivate_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE feed_studyprivate_id_seq OWNED BY feed_studyprivate.id;


--
-- Name: feed_studyprivate_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('feed_studyprivate_id_seq', 15, true);


--
-- Name: feed_subject; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE feed_subject (
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


--
-- Name: feed_subject_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE feed_subject_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: feed_subject_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE feed_subject_id_seq OWNED BY feed_subject.id;


--
-- Name: feed_subject_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('feed_subject_id_seq', 13, true);


--
-- Name: feed_taxon; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE feed_taxon (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    label character varying(255) NOT NULL,
    controlled boolean NOT NULL,
    deprecated boolean NOT NULL,
    genus character varying(255) NOT NULL,
    species character varying(255) NOT NULL,
    common_name character varying(255)
);


--
-- Name: feed_taxon_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE feed_taxon_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: feed_taxon_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE feed_taxon_id_seq OWNED BY feed_taxon.id;


--
-- Name: feed_taxon_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('feed_taxon_id_seq', 8, true);


--
-- Name: feed_technique; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE feed_technique (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    label character varying(255) NOT NULL,
    controlled boolean NOT NULL,
    deprecated boolean NOT NULL
);


--
-- Name: feed_technique_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE feed_technique_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: feed_technique_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE feed_technique_id_seq OWNED BY feed_technique.id;


--
-- Name: feed_technique_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('feed_technique_id_seq', 11, true);


--
-- Name: feed_trial; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE feed_trial (
    id integer NOT NULL,
    created_by_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    session_id integer NOT NULL,
    accession character varying(255),
    "position" integer NOT NULL,
    start timestamp with time zone,
    "end" timestamp with time zone,
    claimed_duration numeric(8,4),
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
    title character varying(255) DEFAULT 'new Trial - edit this'::character varying NOT NULL
);


--
-- Name: feed_trial_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE feed_trial_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: feed_trial_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE feed_trial_id_seq OWNED BY feed_trial.id;


--
-- Name: feed_trial_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('feed_trial_id_seq', 11, true);


--
-- Name: south_migrationhistory; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE south_migrationhistory (
    id integer NOT NULL,
    app_name character varying(255) NOT NULL,
    migration character varying(255) NOT NULL,
    applied timestamp with time zone
);


--
-- Name: south_migrationhistory_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE south_migrationhistory_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: south_migrationhistory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE south_migrationhistory_id_seq OWNED BY south_migrationhistory.id;


--
-- Name: south_migrationhistory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('south_migrationhistory_id_seq', 9, true);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE auth_group ALTER COLUMN id SET DEFAULT nextval('auth_group_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('auth_group_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE auth_message ALTER COLUMN id SET DEFAULT nextval('auth_message_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE auth_permission ALTER COLUMN id SET DEFAULT nextval('auth_permission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE auth_user ALTER COLUMN id SET DEFAULT nextval('auth_user_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE auth_user_groups ALTER COLUMN id SET DEFAULT nextval('auth_user_groups_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('auth_user_user_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE django_admin_log ALTER COLUMN id SET DEFAULT nextval('django_admin_log_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE django_content_type ALTER COLUMN id SET DEFAULT nextval('django_content_type_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE django_site ALTER COLUMN id SET DEFAULT nextval('django_site_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE feed_anteriorposterioraxis ALTER COLUMN id SET DEFAULT nextval('feed_anteriorposterioraxis_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE feed_behavior ALTER COLUMN id SET DEFAULT nextval('feed_behavior_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE feed_channel ALTER COLUMN id SET DEFAULT nextval('feed_channel_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE feed_channellineup ALTER COLUMN id SET DEFAULT nextval('feed_channellineup_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE feed_depthaxis ALTER COLUMN id SET DEFAULT nextval('feed_depthaxis_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE feed_developmentstage ALTER COLUMN id SET DEFAULT nextval('feed_developmentstage_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE feed_dorsalventralaxis ALTER COLUMN id SET DEFAULT nextval('feed_dorsalventralaxis_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE feed_electrodetype ALTER COLUMN id SET DEFAULT nextval('feed_eletrodetype_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE feed_emgelectrode ALTER COLUMN id SET DEFAULT nextval('feed_emgelectrode_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE feed_emgfiltering ALTER COLUMN id SET DEFAULT nextval('feed_emgfiltering_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE feed_emgunit ALTER COLUMN id SET DEFAULT nextval('feed_emgunit_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE feed_experiment ALTER COLUMN id SET DEFAULT nextval('feed_experiment_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE feed_illustration ALTER COLUMN id SET DEFAULT nextval('feed_illustration_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE feed_muscle ALTER COLUMN id SET DEFAULT nextval('feed_muscle_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE feed_restraint ALTER COLUMN id SET DEFAULT nextval('feed_restraint_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE feed_sensor ALTER COLUMN id SET DEFAULT nextval('feed_sensor_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE feed_session ALTER COLUMN id SET DEFAULT nextval('feed_session_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE feed_setup ALTER COLUMN id SET DEFAULT nextval('feed_setup_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE feed_side ALTER COLUMN id SET DEFAULT nextval('feed_side_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE feed_sonounit ALTER COLUMN id SET DEFAULT nextval('feed_sonounit_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE feed_study ALTER COLUMN id SET DEFAULT nextval('feed_study_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE feed_studyprivate ALTER COLUMN id SET DEFAULT nextval('feed_studyprivate_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE feed_subject ALTER COLUMN id SET DEFAULT nextval('feed_subject_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE feed_taxon ALTER COLUMN id SET DEFAULT nextval('feed_taxon_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE feed_technique ALTER COLUMN id SET DEFAULT nextval('feed_technique_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE feed_trial ALTER COLUMN id SET DEFAULT nextval('feed_trial_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE south_migrationhistory ALTER COLUMN id SET DEFAULT nextval('south_migrationhistory_id_seq'::regclass);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: -
--

COPY auth_group (id, name) FROM stdin;
1	contributors
2	terminologists
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY auth_group_permissions (id, group_id, permission_id) FROM stdin;
152	2	25
153	2	26
154	2	27
155	2	28
156	2	29
157	2	30
158	2	31
159	2	32
160	2	33
161	2	34
162	2	35
163	2	36
164	2	37
165	2	38
166	2	39
167	2	40
168	2	41
169	2	42
170	2	43
171	2	44
172	2	45
173	2	46
174	2	47
175	2	48
176	2	49
177	2	50
178	2	51
179	2	52
180	2	53
181	2	54
182	2	55
183	2	56
184	2	57
185	2	58
186	2	59
187	2	60
188	2	61
189	2	62
190	2	63
191	2	64
192	2	65
134	1	97
135	1	67
136	1	100
137	1	70
138	1	103
139	1	73
140	1	106
141	1	76
142	1	109
143	1	79
144	1	112
145	1	82
146	1	115
147	1	85
148	1	118
149	1	88
150	1	91
151	1	94
\.


--
-- Data for Name: auth_message; Type: TABLE DATA; Schema: public; Owner: -
--

COPY auth_message (id, user_id, message) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: -
--

COPY auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add permission	1	add_permission
2	Can change permission	1	change_permission
3	Can delete permission	1	delete_permission
4	Can add group	2	add_group
5	Can change group	2	change_group
6	Can delete group	2	delete_group
7	Can add user	3	add_user
8	Can change user	3	change_user
9	Can delete user	3	delete_user
10	Can add message	4	add_message
11	Can change message	4	change_message
12	Can delete message	4	delete_message
13	Can add content type	5	add_contenttype
14	Can change content type	5	change_contenttype
15	Can delete content type	5	delete_contenttype
16	Can add session	6	add_session
17	Can change session	6	change_session
18	Can delete session	6	delete_session
19	Can add site	7	add_site
20	Can change site	7	change_site
21	Can delete site	7	delete_site
22	Can add log entry	8	add_logentry
23	Can change log entry	8	change_logentry
24	Can delete log entry	8	delete_logentry
25	Can add development stage	9	add_developmentstage
26	Can change development stage	9	change_developmentstage
27	Can delete development stage	9	delete_developmentstage
28	Can add technique	10	add_technique
29	Can change technique	10	change_technique
30	Can delete technique	10	delete_technique
31	Can add behavior	11	add_behavior
32	Can change behavior	11	change_behavior
33	Can delete behavior	11	delete_behavior
34	Can add taxon	12	add_taxon
35	Can change taxon	12	change_taxon
36	Can delete taxon	12	delete_taxon
37	Can add muscle	13	add_muscle
38	Can change muscle	13	change_muscle
39	Can delete muscle	13	delete_muscle
40	Can add side	14	add_side
41	Can change side	14	change_side
42	Can delete side	14	delete_side
43	Can add depth axis	15	add_depthaxis
44	Can change depth axis	15	change_depthaxis
45	Can delete depth axis	15	delete_depthaxis
46	Can add anterior posterior axis	16	add_anteriorposterioraxis
47	Can change anterior posterior axis	16	change_anteriorposterioraxis
48	Can delete anterior posterior axis	16	delete_anteriorposterioraxis
49	Can add dorsal ventral axis	17	add_dorsalventralaxis
50	Can change dorsal ventral axis	17	change_dorsalventralaxis
51	Can delete dorsal ventral axis	17	delete_dorsalventralaxis
55	Can add restraint	19	add_restraint
56	Can change restraint	19	change_restraint
57	Can delete restraint	19	delete_restraint
58	Can add emgunit	20	add_emgunit
59	Can change emgunit	20	change_emgunit
60	Can delete emgunit	20	delete_emgunit
61	Can add sonounit	21	add_sonounit
62	Can change sonounit	21	change_sonounit
63	Can delete sonounit	21	delete_sonounit
64	Can add emgfiltering	22	add_emgfiltering
65	Can change emgfiltering	22	change_emgfiltering
66	Can delete emgfiltering	22	delete_emgfiltering
67	Can add study	23	add_study
68	Can change study	23	change_study
69	Can delete study	23	delete_study
70	Can add study private	24	add_studyprivate
71	Can change study private	24	change_studyprivate
72	Can delete study private	24	delete_studyprivate
73	Can add subject	25	add_subject
74	Can change subject	25	change_subject
75	Can delete subject	25	delete_subject
76	Can add experiment	26	add_experiment
77	Can change experiment	26	change_experiment
78	Can delete experiment	26	delete_experiment
79	Can add setup	27	add_setup
80	Can change setup	27	change_setup
81	Can delete setup	27	delete_setup
82	Can add emgsetup	28	add_emgsetup
83	Can change emgsetup	28	change_emgsetup
84	Can delete emgsetup	28	delete_emgsetup
85	Can add sonosetup	29	add_sonosetup
86	Can change sonosetup	29	change_sonosetup
87	Can delete sonosetup	29	delete_sonosetup
88	Can add sensor	30	add_sensor
89	Can change sensor	30	change_sensor
90	Can delete sensor	30	delete_sensor
91	Can add emgsensor	31	add_emgsensor
92	Can change emgsensor	31	change_emgsensor
93	Can delete emgsensor	31	delete_emgsensor
94	Can add sonosensor	32	add_sonosensor
95	Can change sonosensor	32	change_sonosensor
96	Can delete sonosensor	32	delete_sonosensor
97	Can add channel	33	add_channel
98	Can change channel	33	change_channel
99	Can delete channel	33	delete_channel
100	Can add emgchannel	34	add_emgchannel
101	Can change emgchannel	34	change_emgchannel
102	Can delete emgchannel	34	delete_emgchannel
103	Can add sonochannel	35	add_sonochannel
104	Can change sonochannel	35	change_sonochannel
105	Can delete sonochannel	35	delete_sonochannel
106	Can add session	36	add_session
107	Can change session	36	change_session
108	Can delete session	36	delete_session
109	Can add trial	37	add_trial
110	Can change trial	37	change_trial
111	Can delete trial	37	delete_trial
112	Can add illustration	38	add_illustration
113	Can change illustration	38	change_illustration
114	Can delete illustration	38	delete_illustration
115	Can add channellineup	39	add_channellineup
116	Can change channellineup	39	change_channellineup
117	Can delete channellineup	39	delete_channellineup
118	Can add emgelectrode	40	add_emgelectrode
119	Can change emgelectrode	40	change_emgelectrode
120	Can delete emgelectrode	40	delete_emgelectrode
52	Can add electrode type	18	add_electrodetype
53	Can change electrode type	18	change_electrodetype
54	Can delete electrode type	18	delete_electrodetype
121	Can add migration history	42	add_migrationhistory
122	Can change migration history	42	change_migrationhistory
123	Can delete migration history	42	delete_migrationhistory
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: -
--

COPY auth_user (id, username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined) FROM stdin;
4	provterm2				sha1$958dd$2bb1f547ee7b17f5b6922cb7a6ee352699d0612c	t	t	f	2009-08-10 09:28:35.721766-04	2009-08-06 14:15:59-04
8	german	Rebecca	German		sha1$c9bec$db64de89dd2abf4dad592d2b97aae072eaacfb46	t	t	f	2009-09-09 10:42:10.758206-04	2009-08-10 10:34:03-04
1	xianhua			xl24@duke.edu	sha1$e1b69$1566899ed6de6796850a99e810eac879d094976c	t	t	t	2009-09-09 12:10:42.501471-04	2009-08-04 15:55:36.191288-04
7	wall	Christine	Wall		sha1$37a03$60aa813f0e629da9e5d783847f459b08792d19cf	t	t	f	2009-09-10 10:29:45.834655-04	2009-08-10 10:33:22-04
9	williams	Susan	Williams		sha1$f0b68$c350cedaa816b26f01d59fd9a4bac8c58b574b43	t	t	f	2009-09-10 11:20:07.979851-04	2009-08-10 10:35:08-04
6	vinyard	Chris	Vinyard		sha1$b0bdc$d2c5e9678e062f9672f8ccf6e61329fc9cf7fdd2	t	t	f	2009-09-10 11:57:07.354295-04	2009-08-10 10:32:39-04
2	provider1				sha1$df1b9$58df078f014b5a5cb2f7b0cbd97e296268267efa	t	t	f	2009-08-25 13:39:13.4336-04	2009-08-04 22:48:48-04
5	terminologist3				sha1$4c145$0fc54ddbabb3fc509c6260a95aaed83e3d212cef	t	t	f	2009-08-10 11:58:18.083857-04	2009-08-06 14:25:01-04
16	terminologist				sha1$f0814$9bd2d2d943f3097a1cd57c92b67c46e972608076	t	t	f	2009-09-14 13:44:41-04	2009-09-14 13:44:41-04
3	vgapeyev	Vladimir	Gapeyev	vgapeyev@nescent.org	sha1$44907$9b62d674f8c9f4e460fc887187372fa9d353c6a4	t	t	t	2009-09-14 13:47:01.311707-04	2009-08-06 12:36:37-04
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: -
--

COPY auth_user_groups (id, user_id, group_id) FROM stdin;
1	2	1
3	4	1
4	4	2
6	5	2
7	6	1
8	6	2
9	7	1
10	7	2
13	8	1
14	8	2
15	9	1
16	9	2
24	16	2
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: -
--

COPY django_admin_log (id, action_time, user_id, content_type_id, object_id, object_repr, action_flag, change_message) FROM stdin;
1	2009-08-04 15:57:13.211135-04	1	23	1	xianhua's study 1	1	
2	2009-08-04 15:57:30.688527-04	1	12	1	Genus species	1	
3	2009-08-04 15:57:43.579028-04	1	25	1	xianhua subject 1	1	
4	2009-08-04 15:58:29.672727-04	1	9	1	Stage 1	1	
5	2009-08-04 15:58:32.199137-04	1	26	1	xianhua experiment 1 in study 1 with subject 1	1	
6	2009-08-04 16:01:29.737837-04	1	10	1	EMG	1	
7	2009-08-04 16:01:34.81986-04	1	28	1	EMG setup with preamplifier: 	1	
8	2009-08-04 16:02:54.121496-04	1	13	1	Muscle 1	1	
9	2009-08-04 16:02:59.473848-04	1	14	1	Right	1	
10	2009-08-04 16:03:01.293476-04	1	31	1	EMG Sensor: EMG Channel 1 in EMG Setup 1 of experiment 1 (Muscle: Muscle 1, Side: Right) 	1	
11	2009-08-04 16:04:00.594031-04	1	31	2	EMG Sensor: EMG Channel 2 in EMG Setup 1 of experiment 1 (Muscle: Muscle 1, Side: Right) 	1	
12	2009-08-04 16:13:51.832846-04	1	31	1	EMG Sensor: EMG Channel 1 in EMG Setup 1 of experiment 1 (Muscle: Muscle 1, Side: Right) 	2	No fields changed.
13	2009-08-04 16:22:47.716882-04	1	31	1	EMG Sensor: EMG sensor 1 in EMG Setup 1 of experiment 1 (Muscle: Muscle 1, Side: Right) 	2	Changed name.
14	2009-08-04 16:23:00.932369-04	1	31	2	EMG Sensor: EMG Sensor 2 in EMG Setup 1 of experiment 1 (Muscle: Muscle 1, Side: Right) 	2	Changed name.
15	2009-08-04 16:51:59.035179-04	1	19	1	restraint 1	1	
16	2009-08-04 16:52:01.980183-04	1	36	1	Session 1	1	
17	2009-08-04 17:01:41.571563-04	1	20	1	MH	1	
18	2009-08-04 17:01:50.567299-04	1	22	1	EMG filtering 1	1	
19	2009-08-04 17:02:04.126643-04	1	34	1	EMG Channel: EMG Channel 1 in EMG Setup 1 of experiment 1 (Muscle: Muscle 1, Side: Right) 	1	
20	2009-08-04 17:02:23.660226-04	1	34	2	EMG Channel: EMG Channel 2 in EMG Setup 1 of experiment 1 (Muscle: Muscle 1, Side: Right) 	1	
21	2009-08-04 17:05:09.554812-04	1	26	2	Experiment 2 in study 1 with subject 1	1	
22	2009-08-04 17:05:55.82813-04	1	28	2	EMG setup with preamplifier: 222	1	
23	2009-08-04 17:07:57.949137-04	1	31	3	EMG Sensor: EMG Channel 1 in EMG Setup 2 of experiment 1 (Muscle: Muscle 1, Side: Right) 	1	
24	2009-08-04 17:16:45.452678-04	1	34	3	EMG Channel: EMG Channel 1 in EMG Setup 1 of experiment 2 (Muscle: Muscle 1, Side: Right) 	1	
25	2009-08-04 21:19:28.316905-04	1	39	1	1	1	
26	2009-08-04 22:21:51.266325-04	1	13	2	Muscle 2	1	
27	2009-08-04 22:39:28.379481-04	1	39	1	1	2	No fields changed.
28	2009-08-04 22:40:58.55352-04	1	39	1	1	2	No fields changed.
29	2009-08-04 22:41:57.061994-04	1	11	1	Behavior 1	1	
30	2009-08-04 22:42:48.889032-04	1	37	1	Trail 1	1	
31	2009-08-04 22:48:49.931574-04	1	3	2	prodiver1	1	
32	2009-08-04 22:51:57.237005-04	1	2	1	Data Provider	1	
33	2009-08-04 22:53:40.989766-04	1	3	2	provider1	2	Changed username, is_staff and groups.
34	2009-08-05 11:37:51.009945-04	1	39	2	3	1	
35	2009-08-05 11:42:35.753433-04	1	39	2	2	2	Changed position.
36	2009-08-05 11:42:41.479207-04	1	39	2	2	2	No fields changed.
37	2009-08-05 11:42:43.652384-04	1	39	2	2	2	No fields changed.
38	2009-08-05 11:43:23.551973-04	1	39	2	2	3	
39	2009-08-05 11:44:42.723048-04	1	36	1	Session 1	2	Added channellineup "2".
40	2009-08-05 11:45:05.850897-04	1	36	1	Session 1	2	No fields changed.
41	2009-08-05 11:48:38.22216-04	1	36	1	Session 1	2	No fields changed.
42	2009-08-05 11:50:00.536252-04	1	23	2	study 2	1	
43	2009-08-05 11:50:21.940147-04	1	25	2	sdvsdv	1	
44	2009-08-05 11:52:19.917775-04	1	26	2	Experiment 2 in study 1 with subject 1	2	No fields changed.
45	2009-08-05 11:52:54.844932-04	1	26	2	Experiment 2 in study 1 with subject 1	2	No fields changed.
46	2009-08-05 11:54:23.820349-04	1	26	2	Experiment 2 in study 1 with subject 1	2	No fields changed.
47	2009-08-05 11:54:36.310175-04	1	28	2	EMG setup with preamplifier: 222	2	No fields changed.
48	2009-08-05 14:54:06.215435-04	1	38	1	Illustration object	1	
49	2009-08-05 15:01:45.56556-04	1	38	2	Illustration object	1	
50	2009-08-05 15:11:46.057119-04	1	38	1	Illustration object	2	Changed picture.
51	2009-08-05 16:02:24.484168-04	1	23	2	study 2	2	No fields changed.
52	2009-08-05 16:13:48.058169-04	1	36	1	Session 1	2	No fields changed.
53	2009-08-05 16:45:37.748682-04	1	10	5	Sono	2	No fields changed.
54	2009-08-05 22:24:52.097887-04	1	36	1	Session 1	2	Changed start and end.
55	2009-08-06 12:36:37.544651-04	1	3	3	vgapeyev	1	
56	2009-08-06 12:38:29.655359-04	1	3	3	vgapeyev	2	Changed first_name, last_name, email, is_staff and is_superuser.
57	2009-08-06 12:39:50.456764-04	1	2	1	contributors	2	Changed name.
58	2009-08-06 14:09:43.88738-04	3	2	2	terminologists	1	
59	2009-08-06 14:16:02.318756-04	3	3	4	provterm2	1	
60	2009-08-06 14:16:53.990073-04	3	3	4	provterm2	2	Changed is_staff and groups.
61	2009-08-06 14:23:51.5824-04	3	3	4	provterm2	2	Changed groups.
62	2009-08-06 14:25:03.484568-04	3	3	5	terminologist3	1	
63	2009-08-06 14:25:21.4682-04	3	3	5	terminologist3	2	Changed groups.
64	2009-08-06 14:25:45.491416-04	3	3	5	terminologist3	2	Changed is_staff.
65	2009-08-06 14:27:19.28163-04	5	16	1	Anterior	1	
66	2009-08-06 14:27:34.067641-04	5	16	2	Midline	1	
67	2009-08-06 14:27:54.347239-04	5	16	3	Posterior	1	
68	2009-08-06 14:28:06.31723-04	5	16	2	Midline	2	Changed controlled.
69	2009-08-06 14:30:17.711976-04	1	10	1	EMG	2	No fields changed.
70	2009-08-06 14:37:45.269006-04	5	10	2		3	
71	2009-08-06 14:38:45.236628-04	5	10	3		3	
72	2009-08-06 14:38:48.50352-04	5	10	4		3	
73	2009-08-06 14:39:16.562873-04	5	10	6	EMG	3	
74	2009-08-06 14:39:23.963775-04	5	10	7	Sono	3	
75	2009-08-06 14:40:02.881405-04	5	10	1	EMG	2	Changed controlled.
76	2009-08-06 14:40:22.804942-04	5	10	5	Sono	2	Changed controlled.
77	2009-08-06 14:42:00.837382-04	5	10	8	Bone strain	1	
78	2009-08-06 14:44:12.009894-04	5	10	9	Bite force	1	
79	2009-08-06 14:44:47.712435-04	5	10	10	Pressure	1	
80	2009-08-06 14:45:01.502274-04	5	10	11	Kinematics	1	
81	2009-08-06 15:27:40.518048-04	1	25	2	sdvsdv	2	Changed sex.
82	2009-08-06 15:50:37.536912-04	1	25	2	sdvsdv	2	Changed sex.
83	2009-08-06 21:57:19.622848-04	1	36	1	Session 1	2	Added channellineup "3".
84	2009-08-06 21:57:59.156399-04	1	36	1	Session 1	2	Deleted channellineup "3".
85	2009-08-06 23:00:42.639269-04	2	23	3	Provider1's study	1	
86	2009-08-06 23:01:40.707817-04	2	25	3	provider1's subject 1	1	
87	2009-08-07 11:54:52.930682-04	1	23	2	study 2	3	
88	2009-08-07 11:54:59.761391-04	1	23	1	xianhua's study 1	3	
89	2009-08-07 11:55:03.511739-04	1	23	3	Provider1's study	3	
90	2009-08-07 11:55:22.219807-04	1	12	1	Genus species	3	
91	2009-08-07 11:55:31.645404-04	1	11	1	Behavior 1	3	
92	2009-08-07 11:55:37.231208-04	1	13	2	Muscle 2	3	
93	2009-08-07 11:55:39.317629-04	1	13	1	Muscle 1	3	
94	2009-08-07 11:55:49.709589-04	1	19	1	restraint 1	3	
95	2009-08-07 11:56:03.518768-04	1	9	1	Stage 1	3	
96	2009-08-10 10:11:15.462649-04	3	12	2	Lemur catta	1	
97	2009-08-10 10:11:33.573345-04	3	12	2	Lemur catta	2	Changed controlled.
98	2009-08-10 10:12:35.265209-04	3	12	3	Callithrix jacchus	1	
99	2009-08-10 10:13:09.04894-04	3	12	4	Tupaia balngeri	1	
100	2009-08-10 10:14:03.575355-04	3	12	5	Lama pacos	1	
101	2009-08-10 10:15:19.344711-04	5	11	2	Complete Feeding Sequence	1	
102	2009-08-10 10:15:39.694494-04	5	11	3	Mastication	1	
103	2009-08-10 10:15:51.048205-04	5	11	4	Suckling	1	
104	2009-08-10 10:16:04.207251-04	5	11	5	Swallowing	1	
105	2009-08-10 10:16:13.633546-04	5	11	6	Drinking	1	
106	2009-08-10 10:16:26.168892-04	5	11	7	Ingestion	1	
107	2009-08-10 10:16:42.547656-04	5	11	8	Isometric Bite	1	
108	2009-08-10 10:16:53.983601-04	5	11	9	Intraoral Transport	1	
109	2009-08-10 10:17:18.936137-04	5	13	3	Superficial Masseter	1	
110	2009-08-10 10:17:33.520656-04	5	13	4	Deep Masseter	1	
111	2009-08-10 10:17:46.354611-04	5	13	5	Temporalis	1	
112	2009-08-10 10:18:00.802577-04	5	13	6	Lateral Pterygoid	1	
113	2009-08-10 10:18:13.567312-04	5	13	7	Medial Pterygoid 	1	
114	2009-08-10 10:18:28.313523-04	5	13	8	Anterior Digastric 	1	
115	2009-08-10 10:19:43.980651-04	5	14	1	Right	3	
116	2009-08-10 10:19:52.969599-04	5	14	2	Left	1	
117	2009-08-10 10:20:00.971882-04	5	14	3	Right	1	
118	2009-08-10 10:20:10.99278-04	5	14	4	Midline	1	
119	2009-08-10 10:20:20.743187-04	5	14	5	Unknown	1	
120	2009-08-10 10:20:56.469942-04	5	19	2	None	1	
121	2009-08-10 10:21:04.859642-04	5	19	3	Chair	1	
122	2009-08-10 10:21:12.782832-04	5	19	4	Sling	1	
123	2009-08-10 10:21:27.792032-04	5	19	5	Hand-held	1	
124	2009-08-10 10:21:38.489767-04	5	19	6	Box	1	
125	2009-08-10 10:27:23.261367-04	5	18	1	Surface	1	
126	2009-08-10 10:27:28.744677-04	5	18	2	Indwelling Patch	1	
127	2009-08-10 10:27:43.03226-04	5	18	3	Indwelling Fine-Wire	1	
128	2009-08-10 10:27:51.618703-04	5	18	4	Unknown	1	
129	2009-08-10 10:28:15.426433-04	5	9	2	Infant	1	
130	2009-08-10 10:28:24.853036-04	5	9	3	Juvenile	1	
131	2009-08-10 10:28:35.023424-04	5	9	4	Subadult	1	
132	2009-08-10 10:28:44.168961-04	5	9	5	Adult	1	
133	2009-08-10 10:28:53.994193-04	5	9	6	Unknown	1	
134	2009-08-10 10:29:29.494016-04	5	17	1	Dorsal	1	
135	2009-08-10 10:29:37.115181-04	5	17	2	Ventral	1	
136	2009-08-10 10:30:00.160782-04	5	15	1	Superficial	1	
137	2009-08-10 10:30:10.074658-04	5	15	2	Deep	1	
138	2009-08-10 10:32:39.147527-04	3	3	6	vinyard	1	
139	2009-08-10 10:32:59.452807-04	3	3	6	vinyard	2	Changed first_name, last_name, is_staff and groups.
140	2009-08-10 10:33:22.385296-04	3	3	7	wall	1	
141	2009-08-10 10:33:42.433846-04	3	3	7	wall	2	Changed first_name, last_name, is_staff and groups.
142	2009-08-10 10:34:03.146594-04	3	3	8	german	1	
143	2009-08-10 10:34:21.970207-04	3	3	8	german	2	Changed first_name, last_name and groups.
144	2009-08-10 10:34:33.038416-04	3	3	8	german	2	Changed is_staff.
145	2009-08-10 10:35:08.254788-04	3	3	9	williams	1	
146	2009-08-10 10:35:27.9394-04	3	3	9	williams	2	Changed first_name, last_name, is_staff and groups.
147	2009-08-10 10:50:28.881364-04	6	23	4	BR01RN3 lemur	1	
148	2009-08-10 10:54:39.164956-04	6	23	5	MI99A2 marmoset	1	
149	2009-08-10 11:03:12.32147-04	6	23	6	Treeshrew EMG	1	
150	2009-08-10 11:08:48.393207-04	6	25	4	Brennus	1	
151	2009-08-10 11:11:39.044122-04	6	25	5	Mickey	1	
152	2009-08-10 11:12:27.35916-04	6	25	6	Doughboy	1	
153	2009-08-10 11:17:49.034837-04	6	26	3	<Bogus>	1	
154	2009-08-10 11:22:52.12637-04	6	36	2	Session 1	1	
155	2009-08-10 11:30:44.068824-04	6	37	2	Trail 1	1	
156	2009-08-10 11:35:06.479128-04	6	28	3	EMG setup with preamplifier: Grass	1	
157	2009-08-10 11:57:45.800551-04	6	31	4	EMG Sensor: LSM (Muscle: Superficial Masseter, Side: Left) 	1	
158	2009-08-10 11:59:41.194107-04	5	13	9	Posterior Digastric 	1	
159	2009-08-10 11:59:58.008493-04	5	13	10	Mylohyoid	1	
160	2009-08-10 12:00:07.3679-04	5	13	11	Geniohyoid	1	
161	2009-08-10 12:00:19.87382-04	5	13	12	Genioglossus	1	
162	2009-08-10 12:00:29.681236-04	5	13	13	Hyoglossus	1	
163	2009-08-10 12:00:37.634474-04	5	13	14	Styloglossus	1	
164	2009-08-10 12:00:45.913496-04	5	13	15	Palatoglossus	1	
165	2009-08-10 12:00:57.672833-04	5	13	16	Palatopharyngeus	1	
166	2009-08-10 12:01:18.650425-04	5	13	17	Superior Constrictor 	1	
167	2009-08-10 12:01:32.665143-04	5	13	18	Middle Constrictor 	1	
168	2009-08-10 12:01:42.968264-04	5	13	19	Inferior Constrictor 	1	
169	2009-08-10 12:01:51.473944-04	5	13	20	Omohyoid	1	
170	2009-08-10 12:02:16.856487-04	5	13	21	Sternohyoid	1	
171	2009-08-10 12:02:32.976558-04	5	13	22	Sternothyroid	1	
172	2009-08-10 12:02:47.032307-04	5	13	23	Thyrohyoid	1	
173	2009-08-10 12:11:54.432385-04	6	28	3	EMG setup with preamplifier: Grass	2	Changed notes.
174	2009-08-10 12:18:59.739778-04	6	26	4	<Marmoset experiment>\r\n	1	
175	2009-08-10 12:20:19.681544-04	6	36	3	Session 1	1	
176	2009-08-10 12:22:18.001896-04	6	28	3	EMG setup with preamplifier: Grass	2	Changed notes.
177	2009-08-10 12:23:16.04476-04	6	31	5	EMG Sensor: LDMA (Muscle: Deep Masseter, Side: Left) 	1	
178	2009-08-10 12:23:53.580745-04	6	31	6	EMG Sensor: LDMP (Muscle: Deep Masseter, Side: Left) 	1	
179	2009-08-10 12:24:27.753823-04	6	31	7	EMG Sensor: LPT (Muscle: Temporalis, Side: Left) 	1	
180	2009-08-10 12:25:06.047685-04	6	31	8	EMG Sensor: RSM (Muscle: Superficial Masseter, Side: Right) 	1	
181	2009-08-10 12:25:40.537153-04	6	31	9	EMG Sensor: RDMA (Muscle: Deep Masseter, Side: Right) 	1	
182	2009-08-10 12:26:14.969475-04	6	31	10	EMG Sensor: RDMP (Muscle: Deep Masseter, Side: Right) 	1	
183	2009-08-10 12:26:54.319307-04	6	31	11	EMG Sensor: RPT (Muscle: Temporalis, Side: Right) 	1	
184	2009-08-10 12:30:40.863475-04	6	34	4	EMG Channel: RPT (Muscle: Temporalis, Side: Right) 	1	
185	2009-08-10 12:31:25.91631-04	6	34	5	EMG Channel: RDMP (Muscle: Deep Masseter, Side: Right) 	1	
186	2009-08-10 12:59:07.078379-04	6	34	6	EMG Channel: RDMA (Muscle: Deep Masseter, Side: Right) 	1	
187	2009-08-10 12:59:31.90426-04	6	34	7	EMG Channel: RSM (Muscle: Superficial Masseter, Side: Right) 	1	
188	2009-08-10 13:00:05.144092-04	6	34	8	EMG Channel: LPT (Muscle: Temporalis, Side: Left) 	1	
189	2009-08-10 13:00:26.8585-04	6	34	9	EMG Channel: LDMP (Muscle: Deep Masseter, Side: Left) 	1	
190	2009-08-10 13:00:53.409708-04	6	34	10	EMG Channel: LDMA (Muscle: Deep Masseter, Side: Left) 	1	
191	2009-08-10 13:01:15.44932-04	6	34	11	EMG Channel: LSM (Muscle: Superficial Masseter, Side: Left) 	1	
192	2009-08-10 13:03:22.94559-04	6	36	2	Session 1	2	Added channellineup "1". Added channellineup "2". Added channellineup "3".
193	2009-08-10 13:03:35.81003-04	6	39	8	4	1	
194	2009-08-10 13:03:46.275553-04	6	39	9	5	1	
195	2009-08-10 13:03:58.082592-04	6	39	10	6	1	
196	2009-08-10 13:04:09.130554-04	6	39	11	7	1	
197	2009-08-10 13:04:37.093139-04	6	39	11	7	2	Changed channel.
198	2009-08-10 13:04:48.450665-04	6	39	12	8	1	
199	2009-08-10 13:05:22.427446-04	6	39	10	6	2	Changed channel.
200	2009-08-10 14:18:09.607967-04	8	23	7	infant pig suckling 1	1	
201	2009-08-10 16:38:26.371074-04	1	36	2	Session 1	2	No fields changed.
202	2009-08-11 11:23:07.650795-04	1	36	4	Session 2	1	
203	2009-08-11 11:25:42.154157-04	1	28	4	EMG setup with preamplifier: 	1	
204	2009-08-11 11:37:52.374809-04	1	26	5	test	1	
205	2009-08-11 11:39:04.704943-04	1	36	5	Session 1	1	
206	2009-08-11 11:43:35.046326-04	8	25	7	gandalf	1	
207	2009-08-11 11:44:27.9577-04	1	26	6	test 1	1	
208	2009-08-11 11:44:44.581318-04	8	26	7	suckling data - LOTR pigs 	1	
209	2009-08-11 11:55:12.722947-04	8	36	7	Session 1	1	
210	2009-08-11 11:59:00.780773-04	9	25	8	genevieve	1	
211	2009-08-11 12:29:36.974623-04	1	29	5	Sono setup with sonomicrometer: 	1	
212	2009-08-11 12:29:58.426191-04	1	29	6	Sono setup with sonomicrometer: 	1	
213	2009-08-11 12:31:06.718656-04	1	26	3	<Bogus>	2	Changed bookkeeping.
214	2009-08-11 12:33:26.824718-04	6	29	7	Sono setup with sonomicrometer: 	1	
215	2009-08-11 12:33:45.948935-04	6	32	12	Sono Sensor: crystal 1 (Muscle: Hyoglossus, Side: Midline) 	1	
216	2009-08-11 12:33:56.284592-04	6	32	13	Sono Sensor: crystal 2 (Muscle: Genioglossus, Side: Midline) 	1	
217	2009-08-11 12:35:24.059611-04	6	20	2	Hz	1	
218	2009-08-11 12:36:40.781745-04	6	21	1	mm	1	
219	2009-08-11 12:37:12.203494-04	6	35	12	Sono Channel: sono 12 (Muscle: Hyoglossus, Side: Midline, Crystal1: crystal 1, Crystal2: crystal 2) 	1	
220	2009-08-11 15:36:41.983642-04	8	12	6	Sus scrofa	1	
221	2009-08-12 13:00:37.95335-04	1	28	3	EMG setup with preamplifier: Grass	2	No fields changed.
222	2009-08-12 13:00:50.101346-04	1	28	3	EMG setup with preamplifier: Grass	2	Changed axisdepth for emgsensor "EMG Sensor: LSM (Muscle: Superficial Masseter, Side: Left) ".
223	2009-08-12 13:07:54.958896-04	1	28	3	EMG setup with preamplifier: Grass	2	No fields changed.
224	2009-08-12 13:15:28.959548-04	1	28	3	EMG setup with preamplifier: Grass	2	No fields changed.
225	2009-08-12 13:15:38.077958-04	1	28	3	EMG setup with preamplifier: Grass	2	No fields changed.
226	2009-08-12 13:51:38.283317-04	1	28	3	EMG setup with preamplifier: Grass	2	No fields changed.
227	2009-08-12 13:51:47.841334-04	1	28	3	EMG setup with preamplifier: Grass	2	No fields changed.
228	2009-08-12 13:52:06.790256-04	1	28	3	EMG setup with preamplifier: Grass	2	No fields changed.
229	2009-08-12 13:54:44.624838-04	1	28	3	EMG setup with preamplifier: Grass	2	No fields changed.
230	2009-08-12 14:00:17.12994-04	1	28	3	EMG setup with preamplifier: Grass	2	No fields changed.
231	2009-08-12 14:00:29.987878-04	1	28	3	EMG setup with preamplifier: Grass	2	No fields changed.
232	2009-08-12 14:01:16.37187-04	1	28	3	EMG setup with preamplifier: Grass	2	No fields changed.
233	2009-08-12 14:04:38.177634-04	1	28	3	EMG setup with preamplifier: Grass	2	Changed axisdepth for emgsensor "EMG Sensor: LDMA (Muscle: Deep Masseter, Side: Left) ".
234	2009-08-12 14:04:49.198152-04	1	28	3	EMG setup with preamplifier: Grass	2	No fields changed.
235	2009-08-12 14:05:02.304379-04	1	28	3	EMG setup with preamplifier: Grass	2	No fields changed.
236	2009-08-12 14:05:37.81762-04	1	28	3	EMG setup with preamplifier: Grass	2	No fields changed.
237	2009-08-12 14:06:01.607249-04	1	28	3	EMG setup with preamplifier: Grass	2	No fields changed.
238	2009-08-12 15:50:06.212598-04	1	28	3	EMG setup with preamplifier: Grass	2	Added emgelectrode "electrode 1".
239	2009-08-12 15:50:42.982134-04	1	28	3	EMG setup with preamplifier: Grass	2	Changed muscle for emgelectrode "electrode 1".
240	2009-08-12 15:55:19.758123-04	1	28	3	EMG setup with preamplifier: Grass	2	No fields changed.
241	2009-08-12 15:56:05.257169-04	1	28	3	EMG setup with preamplifier: Grass	2	No fields changed.
242	2009-08-12 15:57:24.482977-04	1	28	3	EMG setup with preamplifier: Grass	2	No fields changed.
243	2009-08-12 16:03:44.324882-04	1	28	3	EMG setup with preamplifier: Grass	2	Added emgelectrode "electrode 2".
244	2009-08-12 16:04:42.435115-04	1	28	3	EMG setup with preamplifier: Grass	2	No fields changed.
245	2009-08-12 16:14:03.718925-04	1	28	3	EMG setup with preamplifier: Grass	2	Deleted emgelectrode "electrode 1".
246	2009-08-12 16:16:45.243644-04	1	36	2	Session 1	2	Added channellineup "9".
247	2009-08-12 16:17:05.716592-04	1	28	3	EMG setup with preamplifier: Grass	2	Deleted emgelectrode "electrode 2".
248	2009-08-12 22:00:30.797005-04	1	28	3	EMG setup with preamplifier: Grass	2	Added emgelectrode "channel 1".
249	2009-08-13 10:32:01.701644-04	1	12	4	Tupaia belangeri	2	Changed species.
250	2009-08-13 14:53:27.461338-04	1	26	3	<Bogus>	2	No fields changed.
251	2009-08-13 14:58:39.155885-04	1	29	7	Sono setup with sonomicrometer: 	2	No fields changed.
252	2009-08-13 15:00:01.275389-04	1	26	3	EMG Experiment of lemurs	2	Changed accession and description.
253	2009-08-13 15:13:36.915268-04	1	28	3	EMG setup with preamplifier: Grass	2	No fields changed.
254	2009-08-13 15:13:48.486917-04	1	26	3	EMG Experiment of lemurs	2	No fields changed.
255	2009-08-13 15:14:09.143921-04	1	29	7	Sono setup with sonomicrometer: 	2	No fields changed.
256	2009-08-13 15:15:32.438207-04	1	28	3	EMG setup with preamplifier: Grass	2	No fields changed.
257	2009-08-14 11:50:40.651456-04	1	36	2	Session 1	2	No fields changed.
258	2009-08-14 12:32:14.440277-04	1	23	5	MI99A2 marmoset	2	No fields changed.
259	2009-08-14 12:36:42.13847-04	1	23	5	MI99A2 marmoset	2	No fields changed.
260	2009-08-14 13:13:26.185984-04	1	23	5	MI99A2 marmoset	2	Changed subj_age for experiment "<Marmoset experiment>\r\n".
261	2009-08-14 13:14:16.345115-04	1	23	5	MI99A2 marmoset	2	Changed subj_weight for experiment "<Marmoset experiment>\r\n".
262	2009-08-14 13:26:22.146262-04	1	36	3	Session 1	2	No fields changed.
263	2009-08-14 13:43:35.102411-04	1	36	3	Session 1	2	No fields changed.
264	2009-08-14 14:17:21.24451-04	1	26	4	<Marmoset experiment>\r\n	2	No fields changed.
265	2009-08-14 14:34:51.019449-04	1	26	4	<Marmoset experiment>\r\n	2	No fields changed.
266	2009-08-14 14:41:49.355779-04	1	26	4	<Marmoset experiment>\r\n	2	No fields changed.
267	2009-08-14 14:42:38.634463-04	1	26	4	<Marmoset experiment>\r\n	2	No fields changed.
268	2009-08-14 15:00:37.548597-04	1	26	4	<Marmoset experiment>\r\n	2	No fields changed.
269	2009-08-14 15:04:01.512134-04	1	26	4	<Marmoset experiment>\r\n	2	No fields changed.
270	2009-08-14 15:05:31.421788-04	1	26	4	<Marmoset experiment>\r\n	2	No fields changed.
271	2009-08-14 15:06:06.093742-04	1	26	4	<Marmoset experiment>\r\n	2	No fields changed.
272	2009-08-14 15:08:12.816133-04	1	26	4	<Marmoset experiment>\r\n	2	No fields changed.
273	2009-08-14 15:09:14.572115-04	1	26	4	<Marmoset experiment>\r\n	2	No fields changed.
274	2009-08-14 15:09:22.680647-04	1	26	4	<Marmoset experiment>\r\n	2	No fields changed.
275	2009-08-14 15:09:38.618951-04	1	26	4	<Marmoset experiment>\r\n	2	No fields changed.
276	2009-08-14 15:09:50.77872-04	1	26	4	<Marmoset experiment>\r\n	2	No fields changed.
277	2009-08-14 15:15:08.701152-04	1	26	4	<Marmoset experiment>\r\n	2	No fields changed.
278	2009-08-14 15:16:00.505879-04	1	26	4	<Marmoset experiment>\r\n	2	No fields changed.
279	2009-08-14 15:16:54.453877-04	1	26	4	<Marmoset experiment>\r\n	2	No fields changed.
280	2009-08-14 15:17:07.220537-04	1	26	4	<Marmoset experiment>\r\n	2	No fields changed.
281	2009-08-14 15:17:30.930722-04	1	26	4	<Marmoset experiment>\r\n	2	No fields changed.
282	2009-08-14 15:17:42.223249-04	1	26	4	<Marmoset experiment>\r\n	2	No fields changed.
283	2009-08-14 15:17:54.517165-04	1	26	4	<Marmoset experiment>\r\n	2	No fields changed.
284	2009-08-14 15:36:39.059904-04	1	29	6	Sono setup with sonomicrometer: 	2	Added sonosensor "Sono Sensor: sono 1 (Muscle: Sternothyroid, Side: Left) ".
285	2009-08-14 15:39:01.769653-04	1	29	6	Sono setup with sonomicrometer: 	2	No fields changed.
286	2009-08-14 15:41:25.858676-04	1	26	5	test	2	No fields changed.
287	2009-08-14 15:54:04.454874-04	1	26	6	test 1	2	No fields changed.
288	2009-08-14 16:20:45.112681-04	3	26	6	test 1	2	No fields changed.
289	2009-08-17 12:39:46.218451-04	1	2	1	contributors	2	Changed permissions.
290	2009-08-21 11:12:57.701069-04	6	23	4	Ring-tailed Lemur EMG	2	Changed name, bookkeeping, start and end.
291	2009-08-21 11:14:56.760457-04	6	12	6	Sus scrofa	2	Changed controlled.
292	2009-08-21 11:15:48.113056-04	6	12	3	Callithrix jacchus	2	Changed label and common_name.
293	2009-08-21 11:15:50.897877-04	6	12	3	Callithrix jacchus	2	No fields changed.
294	2009-08-21 11:18:37.606903-04	6	12	2	Lemur catta	2	Changed common_name.
295	2009-08-21 11:21:00.420027-04	6	23	4	Ring-tailed Lemur EMG	2	Deleted experiment "test 1".
296	2009-08-21 11:25:45.016904-04	6	23	4	Ring-tailed Lemur EMG	2	Changed accession and bookkeeping for experiment "EMG Experiment of lemurs".
297	2009-08-21 11:34:02.475322-04	6	37	2	Trail 1	2	Changed bookkeeping and behavior_notes.
298	2009-08-21 11:35:23.514569-04	6	26	3	EMG Experiment of lemurs	2	No fields changed.
299	2009-08-21 11:57:20.032137-04	6	22	2	band pass	1	
300	2009-08-21 11:57:41.324459-04	6	22	1	EMG filtering 1	2	Changed deprecated.
301	2009-08-21 12:03:14.422689-04	6	18	5	Bipolar indwelling	1	
302	2009-08-21 12:04:25.03023-04	6	28	3	EMG setup with preamplifier: Grass	2	Changed name, notes, muscle, axisdepth, axisap, axisdv and rate for emgelectrode "LSM".
303	2009-08-21 12:04:51.189325-04	6	28	3	EMG setup with preamplifier: Grass	2	Changed notes, eletrode_type and emg_filtering for emgelectrode "LSM".
304	2009-08-21 12:14:13.527333-04	6	28	3	EMG setup with preamplifier: Grass	2	Changed notes. Added emgelectrode "LDMA". Added emgelectrode "LDMP". Added emgelectrode "LPT". Added emgelectrode "RSM". Added emgelectrode "RDMA". Added emgelectrode "RDMP". Added emgelectrode "RPT". Changed notes for emgelectrode "LSM".
305	2009-08-21 12:18:47.782087-04	6	26	3	<descr of Ring-tailed Lemur EMG - experiment	2	Changed description.
306	2009-08-21 12:25:05.263427-04	6	36	2	Session 1	2	Changed subj_notes.
307	2009-08-21 12:26:44.061312-04	6	36	2	Session 1	2	Changed position for channellineup "8". Changed position for channellineup "7".
308	2009-08-21 12:27:01.998594-04	6	36	2	Session 1	2	Changed position for channellineup "8". Changed position for channellineup "7".
309	2009-08-21 12:27:20.186582-04	6	36	2	Session 1	2	Changed position for channellineup "9".
310	2009-08-21 12:27:38.581374-04	6	36	2	Session 1	2	Changed position for channellineup "7".
311	2009-08-21 12:28:45.501039-04	6	36	2	Session 1	2	Changed position for channellineup "8".
312	2009-08-21 12:32:44.591162-04	6	26	3	[# descr of Ring-tailed Lemur EMG - experiment #]	2	Changed description.
313	2009-08-21 14:07:32.344081-04	6	23	5	Marmoset EMG	2	Changed name, bookkeeping, start and end. Changed lab and notes for Study - Private Information "StudyPrivate object".
314	2009-08-21 14:10:18.783594-04	6	23	5	Marmoset EMG	2	Changed end, description, subj_age and subj_weight for experiment "[#descr: Exp1 - Marmoset EMG#]\r\n".
315	2009-08-21 14:12:12.837092-04	6	26	4	[#descr: Exp1 - Marmoset EMG#]\r\n	2	No fields changed.
316	2009-08-21 14:12:23.313252-04	6	26	4	[#descr: Exp1 - Marmoset EMG#]\r\n	2	No fields changed.
317	2009-08-21 14:14:39.080239-04	6	28	28	EMG setup with preamplifier: Grass	2	Changed notes and preamplifier. Added emgelectrode "LSM".
318	2009-08-21 14:23:03.051341-04	6	28	28	EMG setup with preamplifier: Grass	2	Added emgelectrode "LDM". Added emgelectrode "LAT". Added emgelectrode "LPT". Added emgelectrode "RSM". Added emgelectrode "RDM". Added emgelectrode "RAT".
319	2009-08-21 14:23:52.74836-04	6	28	28	EMG setup with preamplifier: Grass	2	Added emgelectrode "RPT".
320	2009-08-21 14:26:47.573078-04	6	36	3	Session 1	2	Added channellineup "1". Added channellineup "2". Added channellineup "3".
321	2009-08-21 14:27:16.232588-04	6	36	3	Session 1	2	Added channellineup "4". Added channellineup "5". Added channellineup "6".
322	2009-08-21 14:27:40.428067-04	6	36	3	Session 1	2	Added channellineup "7". Added channellineup "8".
323	2009-08-21 14:30:45.819169-04	6	36	3	Session 1	2	Added trial "Trail 1".
324	2009-08-21 14:37:03.2989-04	6	23	6	Treeshrew EMG	2	Changed start. Changed notes for Study - Private Information "StudyPrivate object".
325	2009-08-21 14:44:08.367992-04	9	23	8	Alpaca mastication EMGs	1	
326	2009-08-21 14:45:22.152971-04	3	25	8	genevieve	2	Changed study.
327	2009-08-21 14:51:01.307539-04	6	26	8	[#descr Experiment: in Treeshrew EMG #]	1	
328	2009-08-21 15:08:11.067503-04	6	23	5	Marmoset EMG	2	Changed bookkeeping.
329	2009-08-21 15:08:44.740975-04	6	23	6	Treeshrew EMG	2	Changed bookkeeping.
330	2009-08-21 16:07:07.057591-04	6	26	8	[#descr Experiment: in Treeshrew EMG #]	2	No fields changed.
331	2009-08-21 16:08:36.78042-04	6	28	30	EMG setup with preamplifier: 	2	Added EMG electrode "LSM".
332	2009-08-21 16:13:51.303583-04	6	28	30	EMG setup with preamplifier: 	2	Added EMG electrode "LDM". Added EMG electrode "LAT". Added EMG electrode "LPT". Added EMG electrode "RSM". Added EMG electrode "RDM". Added EMG electrode "RAT". Added EMG electrode "RPT".
333	2009-08-21 16:15:44.68039-04	6	28	30	EMG setup with preamplifier: Grass	2	Changed notes and preamplifier.
334	2009-08-21 16:23:25.724893-04	6	36	9	Session 1	2	Added channel lineup "1". Added channel lineup "2". Added channel lineup "3".
335	2009-08-21 16:23:51.824342-04	6	36	9	Session 1	2	Added channel lineup "4". Added channel lineup "5". Added channel lineup "6".
336	2009-08-21 16:24:09.062904-04	6	36	9	Session 1	2	Added channel lineup "7". Added channel lineup "8".
337	2009-08-21 16:26:17.107802-04	6	36	9	Session 1	2	Added trial "Trail 1".
338	2009-08-24 10:23:28.58409-04	9	23	8	Alpaca mastication EMGs	2	Changed name for subject "Perla".
339	2009-08-24 10:28:15.70196-04	9	23	8	Alpaca mastication EMGs	2	Added experiment "".
340	2009-08-24 10:38:28.442769-04	9	26	9	[# Experiment descr - Alpaca mastication EMGs  #] 	2	Changed description.
341	2009-08-24 10:54:29.890596-04	9	26	9	[# Experiment descr - Alpaca mastication EMGs  #] 	2	No fields changed.
342	2009-08-24 11:14:22.568393-04	9	28	32	EMG setup with preamplifier: Grass Model P511	2	Changed notes and preamplifier. Added EMG electrode "LSM".
343	2009-08-24 11:23:56.16863-04	9	28	32	EMG setup with preamplifier: Grass Model P511	2	Changed notes. Added EMG electrode "LDM". Added EMG electrode "LPT". Added EMG electrode "LMP". Added EMG electrode "RSM". Added EMG electrode "RDM". Changed axisap for EMG electrode "LSM".
344	2009-08-24 11:25:21.80435-04	9	28	32	EMG setup with preamplifier: Grass Model P511	2	Added EMG electrode "RPT". Added EMG electrode "RMP".
345	2009-08-24 11:27:12.857789-04	9	28	32	EMG setup with preamplifier: Grass Model P511	2	Changed notes.
346	2009-08-24 12:14:06.689805-04	9	19	7	Other	1	
347	2009-08-24 15:06:09.608016-04	9	36	10	Session 1	2	Changed start.
348	2009-08-24 15:06:28.952589-04	9	36	10	Session 1	2	Changed end.
349	2009-08-24 15:11:31.972762-04	9	36	10	Session 1	2	Changed subj_notes and subj_anesthesia_sedation.
350	2009-08-24 15:12:07.721214-04	9	36	10	Session 1	2	Added channel lineup "1". Added channel lineup "2". Added channel lineup "3".
351	2009-08-24 15:12:47.44188-04	9	36	10	Session 1	2	Added channel lineup "4". Added channel lineup "5". Added channel lineup "6".
352	2009-08-24 15:13:10.799145-04	9	36	10	Session 1	2	Added channel lineup "7". Added channel lineup "8".
353	2009-08-24 15:15:00.225199-04	9	36	10	Session 1	2	Added trial "Trail 1".
354	2009-08-25 12:07:02.092319-04	3	2	2	terminologists	2	Changed permissions.
355	2009-08-25 12:07:06.602988-04	3	2	1	contributors	2	No fields changed.
356	2009-08-25 12:07:24.21617-04	3	2	2	terminologists	2	Changed permissions.
357	2009-08-25 14:44:18.258991-04	6	26	10	x 1	1	
358	2009-08-25 14:47:59.208718-04	6	23	9	study test1 	1	
359	2009-08-25 14:55:13.446833-04	6	23	6	Treeshrew EMG	2	Added experiment "".
360	2009-08-25 15:03:36.090804-04	6	26	13	test 2 experiment	1	
361	2009-08-25 15:06:24.411276-04	6	26	3	[# descr of Ring-tailed Lemur EMG - experiment #]	2	No fields changed.
362	2009-08-25 15:07:39.148464-04	6	26	3	[# descr of Ring-tailed Lemur EMG - experiment #]	2	No fields changed.
363	2009-08-25 15:09:47.405667-04	6	26	14	experiment 3	1	
364	2009-08-25 15:13:26.440848-04	6	23	10	study test 2	1	
365	2009-08-25 15:15:26.37056-04	6	36	11	Session 1	1	
366	2009-08-26 09:31:51.989922-04	6	38	3	Illustration object	1	
367	2009-08-26 09:49:15.392122-04	9	12	7	Capra hircus	1	
368	2009-08-26 09:50:00.808205-04	9	23	11	Goat mastication EMGs	1	
369	2009-08-26 09:52:08.266723-04	9	23	11	Goat mastication EMGs	2	Added subject "Domingo".
370	2009-08-26 09:53:05.263242-04	9	23	11	Goat mastication EMGs	2	No fields changed.
371	2009-08-26 10:05:35.360369-04	9	23	11	Goat mastication EMGs	2	Changed notes for subject "Domingo".
372	2009-08-26 10:06:19.483383-04	9	26	16	[# descr of Exp 1 in Goat Mastication EMG study #] 	1	
373	2009-08-26 10:07:00.304033-04	9	26	16	[# descr of Exp 1 in Goat Mastication EMG study #] 	2	No fields changed.
374	2009-08-26 10:07:35.168909-04	9	26	16	[# descr of Exp 1 in Goat Mastication EMG study #] 	2	No fields changed.
375	2009-08-26 10:11:01.474682-04	9	28	34	EMG setup with preamplifier: Grass Model P511	2	Changed preamplifier.
376	2009-08-26 10:14:13.700765-04	9	28	34	EMG setup with preamplifier: Grass Model P511	2	Added EMG electrode "LSM".
377	2009-08-26 10:19:00.653098-04	9	28	34	EMG setup with preamplifier: Grass Model P511	2	Added EMG electrode "LDM". Added EMG electrode "LPT". Added EMG electrode "LMP". Added EMG electrode "RSM". Added EMG electrode "RDM". Added EMG electrode "RPT". Added EMG electrode "RMP".
378	2009-08-26 10:22:32.295472-04	9	28	34	EMG setup with preamplifier: Grass Model P511	2	Changed notes.
379	2009-08-26 10:35:41.635837-04	9	36	12	Session 1	1	
380	2009-08-26 10:40:51.043825-04	9	36	12	Session 1	2	Added channel lineup "1". Added channel lineup "2". Added channel lineup "3".
381	2009-08-26 10:41:12.256884-04	9	36	12	Session 1	2	Added channel lineup "4". Added channel lineup "5". Added channel lineup "6".
382	2009-08-26 10:41:44.894872-04	9	36	12	Session 1	2	Added channel lineup "7". Added channel lineup "8".
383	2009-08-26 10:42:29.421796-04	9	19	8	Stall	1	
384	2009-08-26 10:42:58.146993-04	9	36	12	Session 1	2	Changed subj_restraint.
385	2009-08-26 10:43:47.070703-04	9	36	10	Session 1	2	Changed subj_notes and subj_restraint.
386	2009-08-26 10:47:09.056168-04	9	37	6	Trail 1	1	
387	2009-08-26 10:47:55.041092-04	6	38	4	Illustration object	1	
388	2009-08-26 10:53:51.868812-04	6	38	4	Illustration object	3	
389	2009-08-26 11:27:18.587168-04	9	26	17	[# test #] 	1	
390	2009-08-26 11:35:59.156316-04	9	26	17	[# test #] 	3	
391	2009-08-26 11:44:27.490842-04	6	26	18	dghjgjghj	1	
392	2009-08-26 11:47:01.333458-04	6	26	19	my test study 	1	
393	2009-08-26 12:04:26.404953-04	6	36	13	Session 1	3	
394	2009-08-26 12:04:59.990597-04	6	26	15		3	
395	2009-08-26 12:06:36.507802-04	6	26	12		3	
396	2009-08-26 12:07:01.083447-04	6	26	11		3	
397	2009-08-26 12:13:35.613809-04	3	23	9	study test1 	3	
398	2009-08-26 12:14:59.704644-04	3	23	10	study test 2	3	
399	2009-08-26 12:18:26.20466-04	3	26	5	test	3	
400	2009-08-26 12:19:17.376275-04	3	26	19	my test study 	3	
401	2009-08-26 12:22:04.577257-04	3	26	18	dghjgjghj	3	
402	2009-08-26 12:22:54.82222-04	6	26	10	x 1	3	
403	2009-08-26 12:26:40.797805-04	9	23	8	Alpaca mastication EMGs	2	Changed bookkeeping.
404	2009-08-26 12:27:49.914001-04	9	23	11	Goat mastication EMGs	2	Changed bookkeeping.
405	2009-08-26 12:29:07.632645-04	9	23	8	Alpaca mastication EMGs	2	Changed bookkeeping.
406	2009-08-26 13:19:05.720818-04	6	36	2	Session 1	2	No fields changed.
407	2009-08-26 13:38:33.487389-04	6	23	6	Treeshrew EMG	2	No fields changed.
408	2009-08-26 13:38:56.189465-04	6	36	9	Session 1	2	No fields changed.
409	2009-08-26 13:39:02.946496-04	6	36	9	Session 1	2	Changed position for Channel Position "7".
410	2009-08-26 13:40:51.376306-04	6	36	9	Session 1	2	No fields changed.
411	2009-08-26 13:40:59.51437-04	6	36	9	Session 1	2	No fields changed.
412	2009-08-26 13:41:26.611186-04	6	36	9	Session 1	2	No fields changed.
413	2009-08-26 13:41:40.066186-04	6	36	9	Session 1	2	Changed position for Channel Position "9".
414	2009-08-26 13:41:53.731533-04	6	36	9	Session 1	2	Changed position for Channel Position "8".
415	2009-08-26 13:47:41.545633-04	6	36	2	Session 1	2	Added trial "Trail 1".
416	2009-08-26 13:48:54.218505-04	6	36	2	Session 1	2	No fields changed.
417	2009-08-26 13:49:18.561683-04	6	36	2	Session 1	2	No fields changed.
418	2009-08-26 13:49:51.617778-04	6	36	2	Session 1	2	No fields changed.
419	2009-08-26 13:52:26.949057-04	6	36	2	Session 1	2	No fields changed.
420	2009-08-26 14:02:53.691367-04	6	36	2	Session 1	2	Changed position for trial "Trail 2".
421	2009-08-26 14:03:40.115729-04	6	36	2	Session 1	2	No fields changed.
422	2009-08-26 14:04:17.690229-04	6	36	2	Session 1	2	No fields changed.
423	2009-08-26 14:06:30.256947-04	6	36	2	Session 1	2	Changed position for trial "Trail 4".
424	2009-08-26 14:09:25.198076-04	6	36	2	Session 1	2	No fields changed.
425	2009-08-26 14:09:41.919019-04	6	36	2	Session 1	2	Changed position for trial "Trail 2".
426	2009-08-26 14:12:45.681866-04	6	36	2	Session 1	2	No fields changed.
427	2009-08-26 14:12:54.920648-04	6	36	2	Session 1	2	Changed position for trial "Trail 3".
428	2009-08-26 14:14:15.273643-04	6	36	2	Session 1	2	Changed position for trial "Trail 2".
429	2009-08-26 14:19:30.856554-04	6	36	2	Session 1	2	Deleted trial "Trail 2".
430	2009-08-26 14:20:14.037428-04	6	36	2	Session 1	2	Added trial "Trail 1".
431	2009-08-26 14:23:48.769476-04	6	36	2	Session 1	2	Deleted trial "Trail 1".
432	2009-08-26 14:24:47.074564-04	6	36	2	Session 1	2	No fields changed.
433	2009-08-26 15:34:25.095212-04	6	36	3	Session 1	2	No fields changed.
434	2009-08-26 15:59:34.750683-04	6	36	3	Session 1	2	No fields changed.
435	2009-08-26 16:22:34.5123-04	6	36	3	Session 1	2	No fields changed.
436	2009-08-26 16:23:34.352279-04	6	36	3	Session 1	2	No fields changed.
437	2009-08-26 16:28:27.879602-04	6	36	3	Session 1	2	No fields changed.
438	2009-08-26 16:36:51.514027-04	6	23	6	Treeshrew EMG	2	Changed sex for subject "Doughboy".
439	2009-08-26 16:43:11.705071-04	6	36	3	Session 1	2	No fields changed.
440	2009-09-02 17:12:59.628376-04	3	23	12	FOO2	1	
441	2009-09-03 09:16:53.748885-04	1	26	20	Experiment: 20	1	
442	2009-09-03 09:46:52.766114-04	1	26	21	Experiment: 21	1	
443	2009-09-03 09:48:38.85349-04	1	26	22	Experiment: 22	1	
444	2009-09-03 09:49:44.610052-04	1	26	23	Experiment: 23	1	
445	2009-09-03 11:25:18.341777-04	1	26	24	Experiment: 24	1	
446	2009-09-03 11:28:34.639554-04	1	26	25	Experiment: 25	1	
447	2009-09-03 12:18:26.881655-04	1	26	26	Experiment: 26	1	
448	2009-09-03 12:19:41.120692-04	1	36	22	Session 3	1	
449	2009-09-03 12:19:51.504205-04	1	36	22	Session 3	3	
450	2009-09-03 13:31:03.833341-04	1	26	27	Experiment: 27	1	
451	2009-09-03 14:36:45.651032-04	1	26	28	Experiment: 28	1	
452	2009-09-03 14:45:21.695078-04	1	26	29	Experiment: 29	1	
453	2009-09-03 17:06:05.463451-04	3	26	30	new Experiment - edit this	1	
454	2009-09-03 17:32:17.301342-04	9	26	9	the only experiment	2	Changed title.
455	2009-09-03 17:38:48.307888-04	9	26	16	Exp 1	2	Changed title.
456	2009-09-03 17:40:16.559606-04	9	36	12	Sess 1	2	Changed title.
457	2009-09-03 17:44:46.304428-04	9	37	5	The only trial	2	Changed title.
458	2009-09-03 17:45:28.829334-04	9	36	10	The only session	2	Changed title and subj_notes.
459	2009-09-04 13:31:47.642128-04	7	23	13	Superficial Temporalis Study	1	
460	2009-09-04 13:32:49.835246-04	7	12	8	Papio anubis	1	
461	2009-09-04 13:33:55.712978-04	7	25	12	Nefertiti 2-11	1	
462	2009-09-04 13:34:47.916139-04	8	23	14	Infant Pig Suckling and Swallowing	1	
463	2009-09-04 13:38:40.162414-04	8	25	13	Meatless	2	Changed notes.
464	2009-09-04 13:39:26.528089-04	7	26	31	new Experiment - edit this	1	
465	2009-09-04 13:40:37.501627-04	7	26	31	Experiment 1	2	Changed title.
466	2009-09-04 13:40:50.071358-04	7	26	31	Experiment 1	2	No fields changed.
467	2009-09-04 13:45:56.034957-04	8	26	32	the only experiment	1	
468	2009-09-04 13:46:52.007355-04	8	25	13	Meatless	2	Changed notes.
469	2009-09-04 13:47:30.748765-04	7	13	24	Deep Anterior Temporalis	1	
470	2009-09-04 13:56:21.488776-04	8	19	9	Unknown	1	
471	2009-09-04 13:59:50.612229-04	7	22	3	Chris Wall's Filtering: 60 Hz Notch Filter	1	
472	2009-09-04 13:59:56.888327-04	7	28	57	EMG setup with preamplifier: 200	2	Changed notes and preamplifier. Added EMG Electrode "DAT".
473	2009-09-04 14:00:05.991916-04	7	28	57	EMG setup with preamplifier: 200	2	Changed emg_filtering for EMG Electrode "DAT".
474	2009-09-04 14:04:46.872903-04	7	28	57	EMG setup with preamplifier: 200	2	Changed muscle, axisdepth and axisap for EMG Electrode "DAT".
475	2009-09-04 14:05:06.031387-04	7	13	24	Deep Anterior Temporalis	3	
476	2009-09-04 14:05:51.522573-04	8	36	24	the only session	1	
477	2009-09-04 14:06:21.541438-04	7	28	57	EMG setup with preamplifier: 200	2	Added EMG Electrode "SAT1".
478	2009-09-04 14:07:52.915038-04	8	26	32	the only experiment	2	No fields changed.
479	2009-09-04 14:08:04.25868-04	7	28	57	EMG setup with preamplifier: 200	2	Added EMG Electrode "SAT2". Added EMG Electrode "PT".
480	2009-09-04 14:12:10.623005-04	7	28	57	EMG setup with preamplifier: 200	2	Changed notes. Changed name for EMG Electrode "EMG Channel 1". Changed name for EMG Electrode "EMG Channel 2". Changed name for EMG Electrode "EMG Channel 3". Changed name for EMG Electrode "EMG Channel 4".
481	2009-09-04 14:13:56.881243-04	8	22	4	60Hz notch	1	
482	2009-09-04 14:14:33.980083-04	8	22	3	Chris Wall's Filtering: 60 Hz Notch Filter, low=100, high=3000	2	Changed label and controlled.
483	2009-09-04 14:15:05.524651-04	7	28	57	EMG setup with preamplifier: 200	2	Added EMG Electrode "EMG Channel 5". Added EMG Electrode "EMG Channel 6". Added EMG Electrode "EMG Channel 7". Added EMG Electrode "EMG Channel 8".
484	2009-09-04 14:20:29.522951-04	8	28	59	EMG setup with preamplifier: Grass	2	Changed notes and preamplifier. Added EMG Electrode "EMG1". Added EMG Electrode "EMG2". Added EMG Electrode "EMG3". Added EMG Electrode "EMG4". Added EMG Electrode "EMG5". Added EMG Electrode "EMG6". Added EMG Electrode "EMG7". Added EMG Electrode "EMG8".
485	2009-09-04 14:21:04.10264-04	8	20	1	MH	3	
486	2009-09-04 14:21:56.868705-04	7	36	23	recording session 1	2	Added Channel Position "1". Added Channel Position "2". Added Channel Position "3".
487	2009-09-04 14:22:11.556492-04	7	36	23	recording session 1	2	Added Channel Position "4". Added Channel Position "5". Added Channel Position "6".
488	2009-09-04 14:22:23.834516-04	7	36	23	recording session 1	2	Added Channel Position "7". Added Channel Position "8".
489	2009-09-04 14:24:56.840869-04	7	11	10	Chewing	1	
490	2009-09-04 14:26:58.31949-04	7	36	23	recording session 1	2	Added trial "new Trial - edit this".
491	2009-09-04 14:27:12.315156-04	8	28	59	EMG setup with preamplifier: Grass	2	Added EMG Electrode "EMG9". Added EMG Electrode "EMG10". Added EMG Electrode "EMG11". Added EMG Electrode "EMG12".
492	2009-09-04 14:28:46.199721-04	7	36	23	recording session 1	2	Changed position, food_type, food_size, behavior_secondary and behavior_notes for trial "new Trial - edit this".
493	2009-09-04 14:34:30.086638-04	8	36	24	the only session	2	Added Channel Position "1". Added Channel Position "2". Added Channel Position "3".
494	2009-09-04 14:34:57.954795-04	8	36	24	the only session	2	Added Channel Position "4". Added Channel Position "5". Added Channel Position "6".
495	2009-09-04 14:35:29.163693-04	8	36	24	the only session	2	Added Channel Position "7". Added Channel Position "8". Added Channel Position "9".
496	2009-09-04 14:35:50.626943-04	8	36	24	the only session	2	Added Channel Position "10". Added Channel Position "11". Added Channel Position "12".
497	2009-09-04 14:36:43.807041-04	8	36	24	the only session	2	Added trial "the only trial".
498	2009-09-04 14:40:44.699077-04	8	37	10	T28	2	Changed title, claimed_duration, subj_treatment, subj_notes, food_type, food_property, behavior_secondary and behavior_notes.
499	2009-09-04 14:53:56.919245-04	1	26	33	new Experiment - edit this	1	
500	2009-09-04 15:20:55.369714-04	7	37	11	new Trial - edit this	1	
501	2009-09-08 17:44:41.963292-04	3	40	48	RMP	2	No fields changed.
502	2009-09-09 11:03:30.182391-04	7	28	57	EMG setup with preamplifier: 200	2	No fields changed.
503	2009-09-09 11:04:00.700016-04	7	28	57	EMG setup with preamplifier: 200	2	Changed name for EMG Electrode "EMG Channel 9".
504	2009-09-09 11:04:26.697511-04	7	28	57	EMG setup with preamplifier: 200	2	Changed name for EMG Electrode "EMG Channel 8".
505	2009-09-09 11:05:01.422587-04	7	28	57	EMG setup with preamplifier: 200	2	Added EMG Electrode "EMG Channel 9".
506	2009-09-09 11:08:13.075483-04	7	28	57	EMG setup with preamplifier: 200	2	No fields changed.
507	2009-09-09 11:08:45.884575-04	7	28	57	EMG setup with preamplifier: 200	2	Deleted EMG Electrode "EMG Channel 9".
508	2009-09-09 11:10:53.316921-04	7	28	57	EMG setup with preamplifier: 200	2	Added EMG Electrode "EMG Channel 10".
509	2009-09-09 11:11:22.53031-04	7	28	57	EMG setup with preamplifier: 200	2	Changed sensor and channel for EMG Electrode "EMG Channel 10".
510	2009-09-09 11:12:48.981029-04	7	28	57	EMG setup with preamplifier: 200	2	Deleted EMG Electrode "EMG Channel 10".
511	2009-09-09 11:26:35.068771-04	7	28	57	EMG setup with preamplifier: 200	2	Added EMG Electrode "EMG Channel 9".
512	2009-09-09 11:33:39.581933-04	7	28	57	EMG setup with preamplifier: 200	2	Added EMG Electrode "EMG Channel 9".
513	2009-09-09 11:39:40.525453-04	7	28	57	EMG setup with preamplifier: 200	2	Added EMG Electrode "EMG Channel 9".
514	2009-09-09 11:42:21.500614-04	7	40	74	EMG Channel 9	3	
515	2009-09-09 11:43:36.163419-04	7	28	57	EMG setup with preamplifier: 200	2	Added EMG Electrode "EMG Channel 9".
516	2009-09-09 11:44:43.533908-04	7	40	75	EMG Channel 9	3	
517	2009-09-09 11:45:24.556987-04	7	28	57	EMG setup with preamplifier: 200	2	Added EMG Electrode "EMG Channel 9".
518	2009-09-09 11:45:35.81734-04	7	28	57	EMG setup with preamplifier: 200	2	Changed name for EMG Electrode "EMG Channel 19".
519	2009-09-09 11:45:48.323466-04	7	28	57	EMG setup with preamplifier: 200	2	Deleted EMG Electrode "EMG Channel 19".
520	2009-09-09 11:53:46.5355-04	7	28	57	EMG setup with preamplifier: 200	2	Added EMG Electrode "EMG Channel 9".
521	2009-09-09 11:54:05.270548-04	7	40	77	EMG Channel 9	3	
522	2009-09-09 11:55:33.458849-04	7	28	57	EMG setup with preamplifier: 200	2	Added EMG Electrode "EMG Channel 9".
523	2009-09-09 11:55:44.937591-04	7	40	78	EMG Channel 9	3	
524	2009-09-09 11:56:47.841483-04	7	28	57	EMG setup with preamplifier: 200	2	Added EMG Electrode "EMG Channel 9".
525	2009-09-09 11:57:00.007077-04	7	40	79	EMG Channel 9	3	
526	2009-09-09 11:57:57.072543-04	7	28	57	EMG setup with preamplifier: 200	2	Added EMG Electrode "EMG Channel 9".
527	2009-09-09 11:58:08.833523-04	7	40	80	EMG Channel 9	3	
528	2009-09-09 12:02:44.091699-04	7	25	12	Nefertiti 2-11	2	No fields changed.
529	2009-09-09 12:10:01.321885-04	7	28	57	EMG setup with preamplifier: 200	2	No fields changed.
530	2009-09-09 12:11:25.295316-04	1	28	34	EMG setup with preamplifier: Grass Model P511	2	No fields changed.
531	2009-09-09 12:13:17.072952-04	7	40	50	EMG Channel 2	2	No fields changed.
532	2009-09-09 12:13:34.443891-04	7	40	50	EMG Channel 22	2	Changed name.
533	2009-09-09 12:15:07.779829-04	7	28	57	EMG setup with preamplifier: 200	2	Changed name for EMG Electrode "EMG Channel 2".
534	2009-09-10 10:34:40.037662-04	7	28	57	EMG setup with preamplifier: Grass	2	Changed notes and preamplifier. Changed name, notes and emg_amplification for EMG Electrode "EMG1".
535	2009-09-10 10:36:49.428431-04	7	28	57	EMG setup with preamplifier: Grass	2	Changed notes. Changed name for EMG Electrode "EMG2". Changed name for EMG Electrode "EMG3". Changed name for EMG Electrode "EMG4". Changed name for EMG Electrode "EMG5".
536	2009-09-10 10:40:44.947473-04	7	28	57	EMG setup with preamplifier: Grass	2	Changed notes. Changed name for EMG Electrode "EMG6". Changed name for EMG Electrode "EMG7". Changed name for EMG Electrode "EMG8".
537	2009-09-10 10:44:55.173962-04	7	28	57	EMG setup with preamplifier: Grass	2	Changed notes.
538	2009-09-10 10:48:12.003918-04	7	28	57	EMG setup with preamplifier: Grass	2	Changed notes and emg_amplification for EMG Electrode "EMG2". Changed notes and emg_amplification for EMG Electrode "EMG3". Changed notes and emg_amplification for EMG Electrode "EMG4".
539	2009-09-10 10:51:07.492969-04	7	28	57	EMG setup with preamplifier: Grass	2	Changed notes and emg_amplification for EMG Electrode "EMG5". Changed notes and emg_amplification for EMG Electrode "EMG6". Changed notes and emg_amplification for EMG Electrode "EMG7". Changed notes and emg_amplification for EMG Electrode "EMG8".
540	2009-09-10 10:56:25.755993-04	7	37	9	Trial 3	2	Changed accession, title, bookkeeping and behavior_notes.
541	2009-09-10 11:03:00.522363-04	7	37	11	new Trial - edit this	3	
542	2009-09-10 11:32:20.544926-04	9	28	32	EMG setup with preamplifier: Grass Model P511	2	Changed emg_amplification for EMG Electrode "LSM".
543	2009-09-10 11:34:12.85217-04	9	28	32	EMG setup with preamplifier: Grass Model P511	2	Changed emg_amplification for EMG Electrode "LDM". Changed emg_amplification for EMG Electrode "LPT". Changed emg_amplification for EMG Electrode "LMP". Changed emg_amplification for EMG Electrode "RSM". Changed emg_amplification for EMG Electrode "RDM". Changed emg_amplification for EMG Electrode "RPT". Changed emg_amplification for EMG Electrode "RMP".
544	2009-09-10 11:45:08.50778-04	9	28	34	EMG setup with preamplifier: Grass Model P511	2	Changed emg_amplification for EMG Electrode "LSM". Changed emg_amplification for EMG Electrode "LDM". Changed emg_amplification for EMG Electrode "LPT". Changed emg_amplification for EMG Electrode "LMP". Changed emg_amplification for EMG Electrode "RSM". Changed emg_amplification for EMG Electrode "RDM". Changed emg_amplification for EMG Electrode "RPT". Changed emg_amplification for EMG Electrode "RMP".
545	2009-09-10 11:46:02.276107-04	9	28	34	EMG setup with preamplifier: Grass Model P511	2	Changed notes.
546	2009-09-10 11:46:56.295139-04	9	28	32	EMG setup with preamplifier: Grass Model P511	2	Changed notes.
547	2009-09-10 11:56:17.565057-04	6	36	21	new Recording Session - edit this	3	
548	2009-09-10 11:59:15.987485-04	6	36	26	FOO session	1	
549	2009-09-10 11:59:35.972671-04	6	36	26	FOO session	3	
550	2009-09-10 12:00:48.190706-04	6	26	3	the only experiment	2	Changed title.
551	2009-09-10 12:12:59.19994-04	6	26	8	the only experiment	2	Changed title.
552	2009-09-10 12:13:38.566087-04	6	26	4	the only experiment	2	Changed title.
553	2009-09-10 12:14:48.467991-04	6	36	2	the only session	2	Changed title.
554	2009-09-10 12:15:20.861255-04	6	36	9	the only session	2	Changed title.
555	2009-09-10 12:15:41.364853-04	6	36	3	the only session	2	Changed title.
556	2009-09-10 12:16:12.122061-04	6	37	2	the only trial	2	Changed title.
557	2009-09-10 12:16:53.319477-04	6	37	3	the only trial	2	Changed title.
558	2009-09-10 12:16:59.18306-04	6	37	3	the only trial	2	No fields changed.
559	2009-09-10 12:17:34.955406-04	6	37	4	the only trial	2	Changed title.
560	2009-09-10 12:47:09.703546-04	3	20	2	volt	2	Changed label.
561	2009-09-10 12:57:37.039428-04	3	20	3	foounit	1	
562	2009-09-10 12:57:53.918162-04	3	20	3	foounit	3	
563	2009-09-10 13:00:03.215552-04	7	36	27	new Recording Session - edit this	1	
564	2009-09-10 13:00:17.335414-04	7	36	27	new Recording Session - edit this	3	
565	2009-09-10 13:02:34.037754-04	7	36	28	new Recording Session - edit this	1	
566	2009-09-10 13:02:40.66923-04	7	36	28	new Recording Session - edit this	3	
567	2009-09-10 13:06:06.061107-04	7	36	29	new Recording Session - edit this	1	
568	2009-09-10 13:06:11.216587-04	7	36	29	new Recording Session - edit this	3	
569	2009-09-10 13:07:46.721496-04	7	40	81	asfrasdf	1	
570	2009-09-10 13:07:58.162647-04	7	40	81	asfrasdf	3	
571	2009-09-10 13:13:07.123335-04	7	40	82	sdfsdfgdsgsdfgvsdfg	1	
572	2009-09-10 13:13:11.906691-04	7	40	82	sdfsdfgdsgsdfgvsdfg	3	
573	2009-09-10 13:13:27.488086-04	7	36	30	new Recording Session - edit this	1	
574	2009-09-10 13:13:41.60733-04	7	36	30	new Recording Session - edit this	3	
575	2009-09-10 13:24:54.047002-04	7	36	23	recording session 1	2	Changed accession.
576	2009-09-10 13:26:29.680469-04	7	36	31	new Recording Session - edit this	1	
577	2009-09-10 13:27:25.100109-04	7	36	31	new Recording Session - edit this	3	
578	2009-09-10 13:28:06.261592-04	7	36	32	new Recording Session - edit this	1	
579	2009-09-10 13:28:20.560464-04	7	36	32	new Recording Session - edit this	3	
580	2009-09-10 13:33:14.870147-04	7	36	33	new Recording Session - edit this	1	
581	2009-09-10 13:33:23.138806-04	7	36	33	new Recording Session - edit this	3	
582	2009-09-10 13:34:19.203242-04	7	36	23	recording session 1	2	No fields changed.
583	2009-09-10 14:00:31.646219-04	3	23	12	FOO2	3	
584	2009-09-10 14:02:00.884682-04	3	23	15	FOO 3	1	
585	2009-09-10 14:02:44.368959-04	3	26	34	new Experiment - edit this	1	
586	2009-09-10 14:04:00.105398-04	3	26	35	Exp 2	1	
587	2009-09-10 14:16:35.041902-04	3	26	34	new Experiment - edit this	3	
588	2009-09-10 14:16:50.793254-04	3	26	35	Exp 2	3	
589	2009-09-14 13:38:35.471363-04	3	3	10	german_contr	1	
590	2009-09-14 13:38:57.907552-04	3	3	10	german_contr	2	Changed is_staff and groups.
591	2009-09-14 13:39:15.758892-04	3	3	11	german_term	1	
592	2009-09-14 13:39:24.515368-04	3	3	11	german_term	2	Changed groups.
593	2009-09-14 13:39:39.561048-04	3	3	11	german_term	2	Changed is_staff.
594	2009-09-14 13:40:10.634649-04	3	3	12	vinyard_contr	1	
595	2009-09-14 13:40:20.454402-04	3	3	12	vinyard_contr	2	Changed is_staff and groups.
596	2009-09-14 13:40:55.533988-04	3	3	13	vinyard_term	1	
597	2009-09-14 13:41:31.125321-04	3	3	13	vinyard_term	2	Changed groups.
598	2009-09-14 13:42:34.606144-04	3	3	11	german_term	3	
599	2009-09-14 13:42:34.620998-04	3	3	13	vinyard_term	3	
600	2009-09-14 13:43:06.050181-04	3	3	14	wall_contr	1	
601	2009-09-14 13:43:19.546677-04	3	3	14	wall_contr	2	Changed is_staff and groups.
602	2009-09-14 13:43:55.027615-04	3	3	15	williams_contr	1	
603	2009-09-14 13:44:09.269387-04	3	3	15	williams_contr	2	Changed is_staff and groups.
604	2009-09-14 13:44:41.88649-04	3	3	16	terminologist	1	
605	2009-09-14 13:44:53.165129-04	3	3	16	terminologist	2	Changed is_staff and groups.
606	2009-09-14 13:47:11.974441-04	3	23	15	FOO 3	3	
607	2009-09-14 13:48:14.009389-04	3	3	10	german_contr	3	
608	2009-09-14 13:48:14.021507-04	3	3	12	vinyard_contr	3	
609	2009-09-14 13:48:14.023737-04	3	3	14	wall_contr	3	
610	2009-09-14 13:48:14.02599-04	3	3	15	williams_contr	3	
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: -
--

COPY django_content_type (id, name, app_label, model) FROM stdin;
1	permission	auth	permission
2	group	auth	group
3	user	auth	user
4	message	auth	message
5	content type	contenttypes	contenttype
6	session	sessions	session
7	site	sites	site
8	log entry	admin	logentry
9	development stage	feed	developmentstage
10	technique	feed	technique
11	behavior	feed	behavior
12	taxon	feed	taxon
13	muscle	feed	muscle
14	side	feed	side
15	depth axis	feed	depthaxis
16	anterior posterior axis	feed	anteriorposterioraxis
17	dorsal ventral axis	feed	dorsalventralaxis
18	eletrode type	feed	eletrodetype
19	restraint	feed	restraint
20	emgunit	feed	emgunit
21	sonounit	feed	sonounit
22	emgfiltering	feed	emgfiltering
23	study	feed	study
24	study private	feed	studyprivate
25	subject	feed	subject
26	experiment	feed	experiment
27	setup	feed	setup
28	emgsetup	feed	emgsetup
29	sonosetup	feed	sonosetup
30	sensor	feed	sensor
31	emgsensor	feed	emgsensor
32	sonosensor	feed	sonosensor
33	channel	feed	channel
34	emgchannel	feed	emgchannel
35	sonochannel	feed	sonochannel
36	session	feed	session
37	trial	feed	trial
38	illustration	feed	illustration
39	channellineup	feed	channellineup
40	emgelectrode	feed	emgelectrode
41	electrode type	feed	electrodetype
42	migration history	south	migrationhistory
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: -
--

COPY django_session (session_key, session_data, expire_date) FROM stdin;
76815d50a97a5e972795386736c3d5ab	gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwZ1LmI5YjU4YWUxZTczMTM4NjcyNWE2\nYjIwYjczNDkyODRl\n	2009-08-25 11:46:55.193325-04
fb46d9775d3b5f698f724dfb7734dd0f	gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwh1LmJmMzYwZDg5MGNhMzZhODY0MGNj\nYTdhM2NiNGY3MmQ1\n	2009-09-18 15:49:25.815089-04
44833eb0fb2e56204a7671023dd25703	gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwN1LjAyYzk3ZDgzYjgxODM4NGM0ZTI4\nNWNiYmY3NjFiNmFh\n	2009-09-22 17:20:12.69728-04
1c64c6e1d246c80183cfdcb46d42aebc	gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwJ1Ljg3OTc5MzAwZmE4M2U1NTRjYWJk\nYjAxOGNmMWM0MDFj\n	2009-08-21 10:10:27.76009-04
0ea291f4ca334928f5f4378cd25672c7	gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwd1LjUwYTc1N2FlMDI0MTliYTJhOTIy\nMDEwOWUzYTJjM2Rk\n	2009-08-25 15:42:36.228333-04
7c8b1055654bce54bd7e5abf31bb70e1	gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjU3N2I3ZGM4ODE5NzhlNWFkOWM2M2FkMjY4\nNzU3N2E5\n	2009-08-22 12:08:06.911364-04
129fe3af8bdc31ae746a9bbe6f5c1cc1	gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwZ1LmI5YjU4YWUxZTczMTM4NjcyNWE2\nYjIwYjczNDkyODRl\n	2009-08-26 12:14:40.997171-04
729de08d58f00fda2ac32d888aab5da1	gAJ9cQEuOGJjOTY5M2I3OWY4M2UzNGM0MjFkZjA5MjBkY2U1NDA=\n	2009-08-26 16:57:46.196551-04
25584339082771e2410c9a403c44e5e5	gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjEzMjQ2NmQ5NGM0ZjRkYjMxODJh\nMDRjOWFmYzQzNDAz\n	2009-09-09 08:35:36.552995-04
f2a36cfdde702265c8c5061257784845	gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwZ1LmI5YjU4YWUxZTczMTM4NjcyNWE2\nYjIwYjczNDkyODRl\n	2009-09-24 11:57:07.378228-04
3c78cd6a0ee8374445aeedddd3da916a	gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwl1LjFlNTA5ZDI0YjRjZDBkYTk4YTVm\nYjE4NGVkMzUzYmQw\n	2009-08-24 14:11:41.375876-04
4c51dfc3bd7b31aaeca3ee2f01e21aca	gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjU3N2I3ZGM4ODE5NzhlNWFkOWM2M2FkMjY4\nNzU3N2E5\n	2009-09-18 14:49:33.13096-04
16f711269d0ee356acdf947500c1a485	gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwN1LjAyYzk3ZDgzYjgxODM4NGM0ZTI4\nNWNiYmY3NjFiNmFh\n	2009-09-24 12:46:46.773942-04
37b5544f78d1ed27a48d636a671e08cb	gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwN1LjAyYzk3ZDgzYjgxODM4NGM0ZTI4\nNWNiYmY3NjFiNmFh\n	2009-09-09 12:21:45.441975-04
b63f6bea70e834e4c1699fe418a14e4c	gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwN1LjU3ZDA0YzM1ODIxMGRkZWE0M2Yz\nYTBhNDNlZTA0ZmZm\n	2009-09-28 13:47:01.334435-04
e6120817921bf4c4d9ec757111b261a3	gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwd1LjUwYTc1N2FlMDI0MTliYTJhOTIy\nMDEwOWUzYTJjM2Rk\n	2009-09-23 12:12:29.020491-04
895c43f8ca18a1f6cbf3170b1e791e1d	gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjkyMWUzZjZlMDJmYjk0MTcyZWNhMjZkNDE3\nOWM4N2E5\n	2009-09-18 13:23:24.138075-04
655a8363e8de3576ccf9b81a04a9e1a6	gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwN1LjAyYzk3ZDgzYjgxODM4NGM0ZTI4\nNWNiYmY3NjFiNmFh\n	2009-09-15 14:10:08.281455-04
7f6f5605d511812ec8151f11d0183a9c	gAJ9cQEuOGJjOTY5M2I3OWY4M2UzNGM0MjFkZjA5MjBkY2U1NDA=\n	2009-08-28 16:41:40.748233-04
01cc48c778abe7b5ae8268ed8b71eee6	gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwN1LjAyYzk3ZDgzYjgxODM4NGM0ZTI4\nNWNiYmY3NjFiNmFh\n	2009-09-15 14:53:27.142575-04
e00ceb5b7273a1fe0e8168f11ac978ff	gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjkyMWUzZjZlMDJmYjk0MTcyZWNhMjZkNDE3\nOWM4N2E5\n	2009-09-16 11:53:25.150449-04
cc938f276ac038088a96a223bc5d8a3d	gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjU3N2I3ZGM4ODE5NzhlNWFkOWM2M2FkMjY4\nNzU3N2E5\n	2009-08-23 20:27:50.870822-04
1da73776941f0440a9055719fe9dee9a	gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwZ1LmI5YjU4YWUxZTczMTM4NjcyNWE2\nYjIwYjczNDkyODRl\n	2009-09-07 15:19:35.590736-04
7e4a09850d3cd4204970ab882298f36f	gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwZ1LmI5YjU4YWUxZTczMTM4NjcyNWE2\nYjIwYjczNDkyODRl\n	2009-08-24 14:11:41.089485-04
1d602dc93d6ed1655919c6ee94bffcc0	gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwh1LmJmMzYwZDg5MGNhMzZhODY0MGNj\nYTdhM2NiNGY3MmQ1\n	2009-08-24 14:11:50.335707-04
dd4e8033680f98fe31f379f417540a89	gAJ9cQEuOGJjOTY5M2I3OWY4M2UzNGM0MjFkZjA5MjBkY2U1NDA=\n	2009-08-20 16:22:08.48728-04
4cc702241783c89d3c86865940367322	gAJ9cQEuOGJjOTY5M2I3OWY4M2UzNGM0MjFkZjA5MjBkY2U1NDA=\n	2009-08-24 15:32:12.723112-04
74ad80767689065533a66102fe2ae6cf	gAJ9cQEuOGJjOTY5M2I3OWY4M2UzNGM0MjFkZjA5MjBkY2U1NDA=\n	2009-08-24 17:01:13.810493-04
6063df2f78da77859d838876ad96175c	gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwN1LjAyYzk3ZDgzYjgxODM4NGM0ZTI4\nNWNiYmY3NjFiNmFh\n	2009-08-25 09:02:02.579331-04
e8641bd363c0f78254c17f35472e47d8	gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjkyMWUzZjZlMDJmYjk0MTcyZWNhMjZkNDE3\nOWM4N2E5\n	2009-09-24 15:33:42.429595-04
\.


--
-- Data for Name: django_site; Type: TABLE DATA; Schema: public; Owner: -
--

COPY django_site (id, domain, name) FROM stdin;
1	example.com	example.com
\.


--
-- Data for Name: feed_anteriorposterioraxis; Type: TABLE DATA; Schema: public; Owner: -
--

COPY feed_anteriorposterioraxis (id, created_by_id, created_at, updated_at, label, controlled, deprecated) FROM stdin;
1	5	2009-08-06 01:00:00-04	2009-08-06 14:27:16.782498-04	Anterior	t	f
3	5	2009-08-06 01:00:00-04	2009-08-06 14:27:54.344355-04	Posterior	t	f
2	5	2009-08-06 01:00:00-04	2009-08-06 14:28:06.313217-04	Midline	t	f
\.


--
-- Data for Name: feed_behavior; Type: TABLE DATA; Schema: public; Owner: -
--

COPY feed_behavior (id, created_by_id, created_at, updated_at, label, controlled, deprecated) FROM stdin;
2	5	2009-08-10 01:00:00-04	2009-08-10 10:15:19.326192-04	Complete Feeding Sequence	t	f
3	5	2009-08-10 01:00:00-04	2009-08-10 10:15:39.692525-04	Mastication	t	f
4	5	2009-08-10 01:00:00-04	2009-08-10 10:15:51.044699-04	Suckling	t	f
5	5	2009-08-10 01:00:00-04	2009-08-10 10:16:04.205226-04	Swallowing	t	f
6	5	2009-08-10 01:00:00-04	2009-08-10 10:16:13.63147-04	Drinking	t	f
7	5	2009-08-10 01:00:00-04	2009-08-10 10:16:26.166704-04	Ingestion	t	f
8	5	2009-08-10 01:00:00-04	2009-08-10 10:16:42.544169-04	Isometric Bite	t	f
9	5	2009-08-10 01:00:00-04	2009-08-10 10:16:53.981622-04	Intraoral Transport	t	f
10	7	2009-09-04 14:24:56.831717-04	2009-09-04 14:24:56.831717-04	Chewing	t	f
\.


--
-- Data for Name: feed_channel; Type: TABLE DATA; Schema: public; Owner: -
--

COPY feed_channel (id, created_by_id, created_at, updated_at, setup_id, name, rate, notes) FROM stdin;
61	8	2009-09-04 14:20:29.391301-04	2009-09-04 14:20:29.391301-04	59	EMG1	6000	
62	8	2009-09-04 14:20:29.405531-04	2009-09-04 14:20:29.405531-04	59	EMG2	6000	
63	8	2009-09-04 14:20:29.420035-04	2009-09-04 14:20:29.420035-04	59	EMG3	6000	
64	8	2009-09-04 14:20:29.433795-04	2009-09-04 14:20:29.433795-04	59	EMG4	6000	
53	7	2009-09-04 13:59:56.705705-04	2009-09-10 10:34:39.999043-04	57	EMG1	10000	\tElectrode Name\t DAT\r\n\tElectrode Type\tI\r\n\tElectrode Location\t1 cm superior to zyg arch\r\n\tImplantation Method\tneedle\r\n\tPosition Verification\tno\r\n
16	\N	2009-08-12 01:00:00-04	2009-08-12 22:00:30.333762-04	3	channel 1	1000	This is a test for chnale 1\r\n
55	7	2009-09-04 14:08:04.227844-04	2009-09-10 10:48:11.957829-04	57	EMG3	10000	\tElectrode Name\tSAT2\r\n\tElectrode Type\tI\r\n\tElectrode Location\t1 cm superior to zyg arch\r\n\tImplantation Method\tneedle\r\n\tPosition Verification\tno\r\n
11	\N	2009-08-12 01:00:00-04	2009-08-21 12:14:13.369943-04	3	LSM	10000	
10	\N	2009-08-21 00:00:00-04	2009-08-21 12:14:13.394462-04	3	LDMA	10000	
9	\N	2009-08-21 00:00:00-04	2009-08-21 12:14:13.415558-04	3	LDMP	10000	
8	\N	2009-08-21 00:00:00-04	2009-08-21 12:14:13.435791-04	3	LPT	10000	
7	\N	2009-08-21 00:00:00-04	2009-08-21 12:14:13.457871-04	3	RSM	10000	
6	\N	2009-08-21 00:00:00-04	2009-08-21 12:14:13.478717-04	3	RDMA	10000	
5	\N	2009-08-21 00:00:00-04	2009-08-21 12:14:13.498915-04	3	RDMP	10000	
4	\N	2009-08-21 00:00:00-04	2009-08-21 12:14:13.519685-04	3	RPT	10000	
17	\N	2009-08-21 00:00:00-04	2009-08-21 14:14:39.076026-04	28	LSM	10000	
18	\N	2009-08-21 00:00:00-04	2009-08-21 14:23:02.973157-04	28	LDM	10000	
19	\N	2009-08-21 00:00:00-04	2009-08-21 14:23:02.987584-04	28	LAT	10000	
20	\N	2009-08-21 00:00:00-04	2009-08-21 14:23:03.000995-04	28	LPT	10000	
21	\N	2009-08-21 00:00:00-04	2009-08-21 14:23:03.015176-04	28	RSM	10000	
22	\N	2009-08-21 00:00:00-04	2009-08-21 14:23:03.029048-04	28	RDM	10000	
23	\N	2009-08-21 00:00:00-04	2009-08-21 14:23:03.045644-04	28	RAT	10000	
24	\N	2009-08-21 00:00:00-04	2009-08-21 14:23:52.743969-04	28	RPT	10000	
25	\N	2009-08-21 00:00:00-04	2009-08-21 16:08:36.776163-04	30	LSM	10000	
26	\N	2009-08-21 00:00:00-04	2009-08-21 16:13:51.216067-04	30	LDM	10000	
27	\N	2009-08-21 00:00:00-04	2009-08-21 16:13:51.230216-04	30	LAT	10000	
28	\N	2009-08-21 00:00:00-04	2009-08-21 16:13:51.244093-04	30	LPT	10000	
29	\N	2009-08-21 00:00:00-04	2009-08-21 16:13:51.257863-04	30	RSM	10000	
30	\N	2009-08-21 00:00:00-04	2009-08-21 16:13:51.271638-04	30	RDM	10000	
31	\N	2009-08-21 00:00:00-04	2009-08-21 16:13:51.285303-04	30	RAT	10000	
32	\N	2009-08-21 00:00:00-04	2009-08-21 16:13:51.299237-04	30	RPT	10000	
56	7	2009-09-04 14:08:04.24539-04	2009-09-10 10:48:11.981176-04	57	EMG4	10000	\tElectrode Name\tPT\r\n\tElectrode Type\tI\r\n\tElectrode Side\tL\r\n\tElectrode Location\tposterior to ear\r\n\tImplantation Method\tneedle\r\n\tPosition Verification\tno\r\n
57	7	2009-09-04 14:15:05.461899-04	2009-09-10 10:51:07.4099-04	57	EMG5	10000	\tElectrode Name\tDAT\r\n\tElectrode Type\tI\r\n\tElectrode Location\t1 cm superior to zyg arch\r\n\tImplantation Method\tneedle\r\n\tPosition Verification\tno
58	7	2009-09-04 14:15:05.481068-04	2009-09-10 10:51:07.425623-04	57	EMG6	10000	\tElectrode Name\tSAT1\r\n\tElectrode Type\tI\r\n\tElectrode Location\t1 cm superior to zyg arch\r\n\tImplantation Method\tneedle\r\n\tPosition Verification\tno\r\n
33	9	2009-08-24 00:00:00-04	2009-09-10 11:32:20.518332-04	32	LSM	10000	
34	9	2009-08-24 00:00:00-04	2009-09-10 11:34:12.752725-04	32	LDM	10000	
65	8	2009-09-04 14:20:29.448332-04	2009-09-04 14:20:29.448332-04	59	EMG5	6000	
66	8	2009-09-04 14:20:29.475217-04	2009-09-04 14:20:29.475217-04	59	EMG6	6000	
67	8	2009-09-04 14:20:29.488264-04	2009-09-04 14:20:29.488264-04	59	EMG7	6000	
68	8	2009-09-04 14:20:29.516996-04	2009-09-04 14:20:29.516996-04	59	EMG8	6000	
69	8	2009-09-04 14:27:12.264791-04	2009-09-04 14:27:12.264791-04	59	EMG9	6000	
70	8	2009-09-04 14:27:12.278017-04	2009-09-04 14:27:12.278017-04	59	EMG10	6000	
71	8	2009-09-04 14:27:12.290509-04	2009-09-04 14:27:12.290509-04	59	EMG11	6000	
72	8	2009-09-04 14:27:12.311246-04	2009-09-04 14:27:12.311246-04	59	EMG12	6000	
54	7	2009-09-04 14:06:21.523508-04	2009-09-10 10:48:11.833141-04	57	EMG2	10000	\tElectrode Name\tSAT1\r\n\tElectrode Type\tI\r\n\tElectrode Location\t1 cm superior to zyg arch\r\n\tImplantation Method\tneedle\r\n\tPosition Verification\tno\r\n
59	7	2009-09-04 14:15:05.494296-04	2009-09-10 10:51:07.441039-04	57	EMG7	10000	\tElectrode Name\tSAT2\r\n\tElectrode Type\tI\r\n\tElectrode Location\t1 cm superior to zyg arch\r\n\tImplantation Method\tneedle\r\n\tPosition Verification\tno\r\n
60	7	2009-09-04 14:15:05.506995-04	2009-09-10 10:51:07.484936-04	57	EMG8	10000	\tElectrode Name\tPT\r\n\tElectrode Type\tI\r\n\tElectrode Location\tposterior to ear\r\n\tImplantation Method\tneedle\r\n\tPosition Verification\tno\r\n
35	9	2009-08-24 00:00:00-04	2009-09-10 11:34:12.768213-04	32	LPT	10000	
36	9	2009-08-24 00:00:00-04	2009-09-10 11:34:12.783267-04	32	LMP	10000	
37	9	2009-08-24 00:00:00-04	2009-09-10 11:34:12.798964-04	32	RSM	10000	
38	9	2009-08-24 00:00:00-04	2009-09-10 11:34:12.814267-04	32	RDM	10000	
39	9	2009-08-24 00:00:00-04	2009-09-10 11:34:12.829461-04	32	RPT	10000	
40	9	2009-08-24 00:00:00-04	2009-09-10 11:34:12.844252-04	32	RMP	10000	
41	9	2009-08-26 00:00:00-04	2009-09-10 11:45:08.390067-04	34	LSM	10000	
42	9	2009-08-26 00:00:00-04	2009-09-10 11:45:08.406258-04	34	LDM	10000	
43	9	2009-08-26 00:00:00-04	2009-09-10 11:45:08.422083-04	34	LPT	10000	
44	9	2009-08-26 00:00:00-04	2009-09-10 11:45:08.43701-04	34	LMP	10000	
45	9	2009-08-26 00:00:00-04	2009-09-10 11:45:08.452092-04	34	RSM	10000	
46	9	2009-08-26 00:00:00-04	2009-09-10 11:45:08.468906-04	34	RDM	10000	
47	9	2009-08-26 00:00:00-04	2009-09-10 11:45:08.484207-04	34	RPT	10000	
48	9	2009-08-26 00:00:00-04	2009-09-10 11:45:08.499847-04	34	RMP	10000	
\.


--
-- Data for Name: feed_channellineup; Type: TABLE DATA; Schema: public; Owner: -
--

COPY feed_channellineup (id, created_by_id, created_at, updated_at, session_id, channel_id, "position") FROM stdin;
5	\N	2009-08-10 01:00:00-04	2009-08-10 13:03:22.895304-04	2	11	1
6	\N	2009-08-10 01:00:00-04	2009-08-10 13:03:22.94137-04	2	10	2
7	\N	2009-08-10 01:00:00-04	2009-08-10 13:03:22.942602-04	2	9	3
8	6	2009-08-10 01:00:00-04	2009-08-10 13:03:35.806596-04	2	8	4
9	6	2009-08-10 01:00:00-04	2009-08-10 13:03:46.272116-04	2	7	5
10	6	2009-08-10 01:00:00-04	2009-08-10 13:05:22.423369-04	2	6	6
11	6	2009-08-10 01:00:00-04	2009-08-21 12:27:01.991529-04	2	5	7
12	6	2009-08-10 01:00:00-04	2009-08-21 12:28:45.493442-04	2	4	8
14	\N	2009-08-21 00:00:00-04	2009-08-21 14:26:47.549394-04	3	17	1
15	\N	2009-08-21 00:00:00-04	2009-08-21 14:26:47.566002-04	3	18	2
16	\N	2009-08-21 00:00:00-04	2009-08-21 14:26:47.567897-04	3	19	3
17	\N	2009-08-21 00:00:00-04	2009-08-21 14:27:16.225063-04	3	20	4
18	\N	2009-08-21 00:00:00-04	2009-08-21 14:27:16.226862-04	3	21	5
19	\N	2009-08-21 00:00:00-04	2009-08-21 14:27:16.228277-04	3	22	6
20	\N	2009-08-21 00:00:00-04	2009-08-21 14:27:40.421914-04	3	23	7
21	\N	2009-08-21 00:00:00-04	2009-08-21 14:27:40.423644-04	3	24	8
22	\N	2009-08-21 00:00:00-04	2009-08-21 16:23:25.717936-04	9	25	1
23	\N	2009-08-21 00:00:00-04	2009-08-21 16:23:25.719436-04	9	26	2
24	\N	2009-08-21 00:00:00-04	2009-08-21 16:23:25.720741-04	9	27	3
25	\N	2009-08-21 00:00:00-04	2009-08-21 16:23:51.816745-04	9	28	4
26	\N	2009-08-21 00:00:00-04	2009-08-21 16:23:51.818523-04	9	29	5
27	\N	2009-08-21 00:00:00-04	2009-08-21 16:23:51.819866-04	9	30	6
28	\N	2009-08-21 00:00:00-04	2009-08-21 16:24:09.057307-04	9	31	7
30	\N	2009-08-24 00:00:00-04	2009-08-24 15:12:07.655628-04	10	33	1
31	\N	2009-08-24 00:00:00-04	2009-08-24 15:12:07.713239-04	10	34	2
32	\N	2009-08-24 00:00:00-04	2009-08-24 15:12:07.715284-04	10	35	3
33	\N	2009-08-24 00:00:00-04	2009-08-24 15:12:47.434345-04	10	36	4
34	\N	2009-08-24 00:00:00-04	2009-08-24 15:12:47.436152-04	10	37	5
35	\N	2009-08-24 00:00:00-04	2009-08-24 15:12:47.437614-04	10	38	6
36	\N	2009-08-24 00:00:00-04	2009-08-24 15:13:10.793171-04	10	39	7
37	\N	2009-08-24 00:00:00-04	2009-08-24 15:13:10.794729-04	10	40	8
38	9	2009-08-26 00:00:00-04	2009-08-26 10:40:51.021855-04	12	41	1
39	9	2009-08-26 00:00:00-04	2009-08-26 10:40:51.037864-04	12	42	2
40	9	2009-08-26 00:00:00-04	2009-08-26 10:40:51.039359-04	12	43	3
41	9	2009-08-26 00:00:00-04	2009-08-26 10:41:12.24962-04	12	44	4
42	9	2009-08-26 00:00:00-04	2009-08-26 10:41:12.251264-04	12	45	5
43	9	2009-08-26 00:00:00-04	2009-08-26 10:41:12.252653-04	12	46	6
44	9	2009-08-26 00:00:00-04	2009-08-26 10:41:44.887349-04	12	47	7
45	9	2009-08-26 00:00:00-04	2009-08-26 10:41:44.889396-04	12	48	8
29	6	2009-08-21 00:00:00-04	2009-08-26 13:41:53.715281-04	9	28	8
46	7	2009-09-04 14:21:56.812467-04	2009-09-04 14:21:56.812467-04	23	53	1
47	7	2009-09-04 14:21:56.862046-04	2009-09-04 14:21:56.862046-04	23	54	2
48	7	2009-09-04 14:21:56.863039-04	2009-09-04 14:21:56.863039-04	23	55	3
49	7	2009-09-04 14:22:11.548767-04	2009-09-04 14:22:11.548767-04	23	56	4
50	7	2009-09-04 14:22:11.550187-04	2009-09-04 14:22:11.550187-04	23	57	5
51	7	2009-09-04 14:22:11.551188-04	2009-09-04 14:22:11.551188-04	23	58	6
52	7	2009-09-04 14:22:23.829262-04	2009-09-04 14:22:23.829262-04	23	59	7
53	7	2009-09-04 14:22:23.83068-04	2009-09-04 14:22:23.83068-04	23	60	8
54	8	2009-09-04 14:34:30.080239-04	2009-09-04 14:34:30.080239-04	24	61	1
55	8	2009-09-04 14:34:30.081824-04	2009-09-04 14:34:30.081824-04	24	62	2
56	8	2009-09-04 14:34:30.082828-04	2009-09-04 14:34:30.082828-04	24	63	3
57	8	2009-09-04 14:34:57.948317-04	2009-09-04 14:34:57.948317-04	24	64	4
58	8	2009-09-04 14:34:57.949958-04	2009-09-04 14:34:57.949958-04	24	65	5
59	8	2009-09-04 14:34:57.950953-04	2009-09-04 14:34:57.950953-04	24	66	6
60	8	2009-09-04 14:35:29.156272-04	2009-09-04 14:35:29.156272-04	24	67	7
61	8	2009-09-04 14:35:29.157689-04	2009-09-04 14:35:29.157689-04	24	68	8
62	8	2009-09-04 14:35:29.158931-04	2009-09-04 14:35:29.158931-04	24	69	9
63	8	2009-09-04 14:35:50.620114-04	2009-09-04 14:35:50.620114-04	24	70	10
64	8	2009-09-04 14:35:50.621737-04	2009-09-04 14:35:50.621737-04	24	71	11
65	8	2009-09-04 14:35:50.622732-04	2009-09-04 14:35:50.622732-04	24	72	12
\.


--
-- Data for Name: feed_depthaxis; Type: TABLE DATA; Schema: public; Owner: -
--

COPY feed_depthaxis (id, created_by_id, created_at, updated_at, label, controlled, deprecated) FROM stdin;
1	5	2009-08-10 01:00:00-04	2009-08-10 10:30:00.13771-04	Superficial	t	f
2	5	2009-08-10 01:00:00-04	2009-08-10 10:30:10.071201-04	Deep	t	f
\.


--
-- Data for Name: feed_developmentstage; Type: TABLE DATA; Schema: public; Owner: -
--

COPY feed_developmentstage (id, created_by_id, created_at, updated_at, label, controlled, deprecated) FROM stdin;
2	5	2009-08-10 01:00:00-04	2009-08-10 10:28:15.375808-04	Infant	t	f
3	5	2009-08-10 01:00:00-04	2009-08-10 10:28:24.849533-04	Juvenile	t	f
4	5	2009-08-10 01:00:00-04	2009-08-10 10:28:35.02169-04	Subadult	t	f
5	5	2009-08-10 01:00:00-04	2009-08-10 10:28:44.167237-04	Adult	t	f
6	5	2009-08-10 01:00:00-04	2009-08-10 10:28:53.990777-04	Unknown	t	f
\.


--
-- Data for Name: feed_dorsalventralaxis; Type: TABLE DATA; Schema: public; Owner: -
--

COPY feed_dorsalventralaxis (id, created_by_id, created_at, updated_at, label, controlled, deprecated) FROM stdin;
1	5	2009-08-10 01:00:00-04	2009-08-10 10:29:29.489182-04	Dorsal	t	f
2	5	2009-08-10 01:00:00-04	2009-08-10 10:29:37.111709-04	Ventral	t	f
\.


--
-- Data for Name: feed_electrodetype; Type: TABLE DATA; Schema: public; Owner: -
--

COPY feed_electrodetype (id, created_by_id, created_at, updated_at, label, controlled, deprecated) FROM stdin;
1	5	2009-08-10 01:00:00-04	2009-08-10 10:27:23.207984-04	Surface	t	f
2	5	2009-08-10 01:00:00-04	2009-08-10 10:27:28.742804-04	Indwelling Patch	t	f
3	5	2009-08-10 01:00:00-04	2009-08-10 10:27:43.030368-04	Indwelling Fine-Wire	t	f
4	5	2009-08-10 01:00:00-04	2009-08-10 10:27:51.615139-04	Unknown	t	f
5	6	2009-08-21 00:00:00-04	2009-08-21 12:03:14.386487-04	Bipolar indwelling	t	f
\.


--
-- Data for Name: feed_emgchannel; Type: TABLE DATA; Schema: public; Owner: -
--

COPY feed_emgchannel (channel_ptr_id, sensor_id, emg_unit_id, emg_filtering_id, emg_amplification) FROM stdin;
16	16	2	1	\N
11	4	2	2	\N
10	5	2	2	\N
9	6	2	2	\N
8	7	2	2	\N
7	8	2	2	\N
6	9	2	2	\N
5	10	2	2	\N
4	11	2	2	\N
17	18	2	2	\N
18	19	2	2	\N
19	20	2	2	\N
20	21	2	2	\N
21	22	2	2	\N
22	23	2	2	\N
23	24	2	2	\N
24	25	2	2	\N
25	26	2	2	\N
26	27	2	2	\N
27	28	2	2	\N
28	29	2	2	\N
29	30	2	2	\N
30	31	2	2	\N
31	32	2	2	\N
32	33	2	2	\N
33	34	2	2	\N
34	35	2	2	\N
35	36	2	2	\N
36	37	2	2	\N
37	38	2	2	\N
38	39	2	2	\N
39	40	2	2	\N
40	41	2	2	\N
41	42	2	2	\N
42	43	2	2	\N
43	44	2	2	\N
44	45	2	2	\N
45	46	2	2	\N
46	47	2	2	\N
47	48	2	2	\N
53	54	2	3	\N
54	55	2	3	\N
55	56	2	3	\N
56	57	2	3	\N
57	58	2	3	\N
58	59	2	3	\N
59	60	2	3	\N
60	61	2	3	\N
61	62	2	4	\N
62	63	2	4	\N
63	64	2	4	\N
64	65	2	4	\N
65	66	2	4	\N
66	67	2	4	\N
67	68	2	4	\N
68	69	2	4	\N
69	70	2	4	\N
70	71	2	4	\N
71	72	2	4	\N
72	73	2	4	\N
48	49	2	2	\N
\.


--
-- Data for Name: feed_emgelectrode; Type: TABLE DATA; Schema: public; Owner: -
--

COPY feed_emgelectrode (id, created_by_id, created_at, updated_at, setup_id, name, notes, muscle_id, side_id, axisdepth_id, axisap_id, axisdv_id, electrode_type_id, rate, emg_unit_id, emg_filtering_id, emg_amplification, channel_id, sensor_id) FROM stdin;
24	6	2009-08-21 00:00:00-04	2009-08-21 16:08:36.762679-04	30	LSM		3	2	\N	\N	\N	5	10000	2	2	\N	25	26
25	6	2009-08-21 00:00:00-04	2009-08-21 16:13:51.20399-04	30	LDM		4	2	\N	\N	\N	5	10000	2	2	\N	26	27
26	6	2009-08-21 00:00:00-04	2009-08-21 16:13:51.220649-04	30	LAT		5	2	\N	1	\N	5	10000	2	2	\N	27	28
27	6	2009-08-21 00:00:00-04	2009-08-21 16:13:51.234493-04	30	LPT		5	2	\N	3	\N	5	10000	2	2	\N	28	29
28	6	2009-08-21 00:00:00-04	2009-08-21 16:13:51.24824-04	30	RSM		3	3	\N	\N	\N	5	10000	2	2	\N	29	30
29	6	2009-08-21 00:00:00-04	2009-08-21 16:13:51.262087-04	30	RDM		4	3	\N	\N	\N	5	10000	2	2	\N	30	31
30	6	2009-08-21 00:00:00-04	2009-08-21 16:13:51.2758-04	30	RAT		5	3	\N	1	\N	5	10000	2	2	\N	31	32
31	6	2009-08-21 00:00:00-04	2009-08-21 16:13:51.289559-04	30	RPT		5	3	\N	3	\N	5	10000	2	2	\N	32	33
16	6	2009-08-21 00:00:00-04	2009-08-21 14:14:39.052428-04	28	LSM		3	2	\N	\N	\N	5	10000	2	2	\N	17	18
17	6	2009-08-21 00:00:00-04	2009-08-21 14:23:02.961148-04	28	LDM		4	2	\N	\N	\N	5	10000	2	2	\N	18	19
18	6	2009-08-21 00:00:00-04	2009-08-21 14:23:02.977202-04	28	LAT		5	2	\N	1	\N	5	10000	2	2	\N	19	20
19	6	2009-08-21 00:00:00-04	2009-08-21 14:23:02.991564-04	28	LPT		5	2	\N	3	\N	5	10000	2	2	\N	20	21
20	6	2009-08-21 00:00:00-04	2009-08-21 14:23:03.005021-04	28	RSM		3	3	\N	\N	\N	5	10000	2	2	\N	21	22
21	6	2009-08-21 00:00:00-04	2009-08-21 14:23:03.019189-04	28	RDM		4	3	\N	\N	\N	5	10000	2	2	\N	22	23
22	6	2009-08-21 00:00:00-04	2009-08-21 14:23:03.03345-04	28	RAT		5	3	\N	1	\N	5	10000	2	2	\N	23	24
23	6	2009-08-21 00:00:00-04	2009-08-21 14:23:52.731322-04	28	RPT		5	3	\N	3	\N	5	10000	2	2	\N	24	25
8	6	2009-08-12 01:00:00-04	2009-08-21 12:14:13.345612-04	3	LSM		3	2	\N	\N	\N	5	10000	2	2	\N	11	4
9	6	2009-08-21 00:00:00-04	2009-08-21 12:14:13.380186-04	3	LDMA		4	2	\N	1	\N	5	10000	2	2	\N	10	5
10	6	2009-08-21 00:00:00-04	2009-08-21 12:14:13.402261-04	3	LDMP		4	2	\N	3	\N	5	10000	2	2	\N	9	6
11	6	2009-08-21 00:00:00-04	2009-08-21 12:14:13.423007-04	3	LPT		5	2	\N	3	\N	5	10000	2	2	\N	8	7
12	6	2009-08-21 00:00:00-04	2009-08-21 12:14:13.444652-04	3	RSM		3	3	\N	\N	\N	5	10000	2	2	\N	7	8
13	6	2009-08-21 00:00:00-04	2009-08-21 12:14:13.465416-04	3	RDMA		4	3	\N	1	\N	5	10000	2	2	\N	6	9
14	6	2009-08-21 00:00:00-04	2009-08-21 12:14:13.486049-04	3	RDMP		4	3	\N	3	\N	5	10000	2	2	\N	5	10
15	6	2009-08-21 00:00:00-04	2009-08-21 12:14:13.50652-04	3	RPT		5	3	\N	3	\N	5	10000	2	2	\N	4	11
57	8	2009-09-04 14:20:29.375149-04	2009-09-04 14:20:29.375149-04	59	EMG1		10	3	\N	\N	\N	4	6000	2	4	\N	61	62
58	8	2009-09-04 14:20:29.396112-04	2009-09-04 14:20:29.396112-04	59	EMG2		21	3	\N	\N	\N	4	6000	2	4	\N	62	63
59	8	2009-09-04 14:20:29.410136-04	2009-09-04 14:20:29.410136-04	59	EMG3		11	2	\N	\N	\N	4	6000	2	4	\N	63	64
60	8	2009-09-04 14:20:29.424175-04	2009-09-04 14:20:29.424175-04	59	EMG4		10	2	\N	\N	\N	4	6000	2	4	\N	64	65
61	8	2009-09-04 14:20:29.43811-04	2009-09-04 14:20:29.43811-04	59	EMG5		21	2	\N	\N	\N	4	6000	2	4	\N	65	66
62	8	2009-09-04 14:20:29.466094-04	2009-09-04 14:20:29.466094-04	59	EMG6		11	2	\N	\N	\N	4	6000	2	4	\N	66	67
49	7	2009-09-04 13:59:56.705705-04	2009-09-10 10:34:40.004073-04	57	EMG1	\tElectrode Name\t DAT\r\n\tElectrode Type\tI\r\n\tElectrode Location\t1 cm superior to zyg arch\r\n\tImplantation Method\tneedle\r\n\tPosition Verification\tno\r\n	5	2	2	1	\N	3	10000	2	3	200	53	54
33	9	2009-08-24 00:00:00-04	2009-09-10 11:32:20.522491-04	32	LSM		3	2	\N	3	\N	5	10000	2	2	2000	33	34
63	8	2009-09-04 14:20:29.479025-04	2009-09-04 14:20:29.479025-04	59	EMG7		20	2	\N	\N	\N	4	6000	2	4	\N	67	68
64	8	2009-09-04 14:20:29.492026-04	2009-09-04 14:20:29.492026-04	59	EMG8		13	2	\N	\N	\N	4	6000	2	4	\N	68	69
65	8	2009-09-04 14:27:12.253507-04	2009-09-04 14:27:12.253507-04	59	EMG9		7	2	\N	\N	\N	4	6000	2	4	\N	69	70
66	8	2009-09-04 14:27:12.268873-04	2009-09-04 14:27:12.268873-04	59	EMG10		20	3	\N	\N	\N	4	6000	2	4	\N	70	71
67	8	2009-09-04 14:27:12.281824-04	2009-09-04 14:27:12.281824-04	59	EMG11		13	3	\N	\N	\N	4	6000	2	4	\N	71	72
68	8	2009-09-04 14:27:12.294328-04	2009-09-04 14:27:12.294328-04	59	EMG12		7	2	\N	\N	\N	4	6000	2	4	\N	72	73
55	7	2009-09-04 14:15:05.494296-04	2009-09-10 10:51:07.472016-04	57	EMG7	\tElectrode Name\tSAT2\r\n\tElectrode Type\tI\r\n\tElectrode Location\t1 cm superior to zyg arch\r\n\tImplantation Method\tneedle\r\n\tPosition Verification\tno\r\n	5	3	1	1	\N	3	10000	2	3	1000	59	60
56	7	2009-09-04 14:15:05.506995-04	2009-09-10 10:51:07.488393-04	57	EMG8	\tElectrode Name\tPT\r\n\tElectrode Type\tI\r\n\tElectrode Location\tposterior to ear\r\n\tImplantation Method\tneedle\r\n\tPosition Verification\tno\r\n	5	3	\N	3	\N	3	10000	2	3	500	60	61
50	7	2009-09-04 14:06:21.523508-04	2009-09-10 10:48:11.836704-04	57	EMG2	\tElectrode Name\tSAT1\r\n\tElectrode Type\tI\r\n\tElectrode Location\t1 cm superior to zyg arch\r\n\tImplantation Method\tneedle\r\n\tPosition Verification\tno\r\n	5	2	1	1	\N	3	10000	2	3	500	54	55
51	7	2009-09-04 14:08:04.227844-04	2009-09-10 10:48:11.963458-04	57	EMG3	\tElectrode Name\tSAT2\r\n\tElectrode Type\tI\r\n\tElectrode Location\t1 cm superior to zyg arch\r\n\tImplantation Method\tneedle\r\n\tPosition Verification\tno\r\n	5	2	1	1	\N	3	10000	2	3	500	55	56
52	7	2009-09-04 14:08:04.24539-04	2009-09-10 10:48:11.986085-04	57	EMG4	\tElectrode Name\tPT\r\n\tElectrode Type\tI\r\n\tElectrode Side\tL\r\n\tElectrode Location\tposterior to ear\r\n\tImplantation Method\tneedle\r\n\tPosition Verification\tno\r\n	5	2	\N	3	\N	3	10000	2	3	500	56	57
53	7	2009-09-04 14:15:05.461899-04	2009-09-10 10:51:07.413503-04	57	EMG5	\tElectrode Name\tDAT\r\n\tElectrode Type\tI\r\n\tElectrode Location\t1 cm superior to zyg arch\r\n\tImplantation Method\tneedle\r\n\tPosition Verification\tno	5	3	2	1	\N	3	10000	2	3	100	57	58
54	7	2009-09-04 14:15:05.481068-04	2009-09-10 10:51:07.428995-04	57	EMG6	\tElectrode Name\tSAT1\r\n\tElectrode Type\tI\r\n\tElectrode Location\t1 cm superior to zyg arch\r\n\tImplantation Method\tneedle\r\n\tPosition Verification\tno\r\n	5	3	1	1	\N	3	10000	2	3	1000	58	59
34	9	2009-08-24 00:00:00-04	2009-09-10 11:34:12.756035-04	32	LDM		4	2	\N	3	\N	5	10000	2	2	500	34	35
35	9	2009-08-24 00:00:00-04	2009-09-10 11:34:12.771553-04	32	LPT		5	2	\N	3	\N	5	10000	2	2	5000	35	36
36	9	2009-08-24 00:00:00-04	2009-09-10 11:34:12.787161-04	32	LMP		7	2	\N	\N	\N	5	10000	2	2	2000	36	37
37	9	2009-08-24 00:00:00-04	2009-09-10 11:34:12.80244-04	32	RSM		3	3	\N	3	\N	5	10000	2	2	1000	37	38
38	9	2009-08-24 00:00:00-04	2009-09-10 11:34:12.817654-04	32	RDM		4	3	\N	3	\N	5	10000	2	2	1000	38	39
39	9	2009-08-24 00:00:00-04	2009-09-10 11:34:12.832767-04	32	RPT		5	3	\N	3	\N	5	10000	2	2	100	39	40
40	9	2009-08-24 00:00:00-04	2009-09-10 11:34:12.84765-04	32	RMP		7	3	\N	\N	\N	5	10000	2	2	1000	40	41
41	9	2009-08-26 00:00:00-04	2009-09-10 11:45:08.393784-04	34	LSM		3	2	\N	3	\N	5	10000	2	2	1000	41	42
42	9	2009-08-26 00:00:00-04	2009-09-10 11:45:08.409703-04	34	LDM		4	2	\N	3	\N	5	10000	2	2	1000	42	43
43	9	2009-08-26 00:00:00-04	2009-09-10 11:45:08.425415-04	34	LPT		5	2	\N	3	\N	5	10000	2	2	1000	43	44
44	9	2009-08-26 00:00:00-04	2009-09-10 11:45:08.440309-04	34	LMP		7	2	\N	\N	\N	5	10000	2	2	1000	44	45
45	9	2009-08-26 00:00:00-04	2009-09-10 11:45:08.455468-04	34	RSM		3	3	\N	3	\N	5	10000	2	2	2000	45	46
46	9	2009-08-26 00:00:00-04	2009-09-10 11:45:08.472272-04	34	RDM		4	3	\N	3	\N	5	10000	2	2	1000	46	47
47	9	2009-08-26 00:00:00-04	2009-09-10 11:45:08.487396-04	34	RPT		5	3	\N	3	\N	5	10000	2	2	10000	47	48
48	9	2009-08-26 00:00:00-04	2009-09-10 11:45:08.503299-04	34	RMP		7	3	\N	\N	\N	5	10000	2	2	200	48	49
\.


--
-- Data for Name: feed_emgfiltering; Type: TABLE DATA; Schema: public; Owner: -
--

COPY feed_emgfiltering (id, created_by_id, created_at, updated_at, label, controlled, deprecated) FROM stdin;
2	6	2009-08-21 00:00:00-04	2009-08-21 11:57:20.001983-04	band pass	t	f
1	1	2009-08-04 01:00:00-04	2009-08-21 11:57:41.320465-04	EMG filtering 1	f	t
4	8	2009-09-04 14:13:56.877661-04	2009-09-04 14:13:56.877661-04	60Hz notch	t	f
3	8	2009-09-04 13:59:50.579305-04	2009-09-04 14:14:33.966636-04	Chris Wall's Filtering: 60 Hz Notch Filter, low=100, high=3000	t	f
\.


--
-- Data for Name: feed_emgsensor; Type: TABLE DATA; Schema: public; Owner: -
--

COPY feed_emgsensor (sensor_ptr_id, muscle_id, side_id, axisdepth_id, axisap_id, axisdv_id, electrode_type_id) FROM stdin;
16	13	2	2	1	2	3
4	3	2	\N	\N	\N	5
5	4	2	\N	1	\N	5
6	4	2	\N	3	\N	5
7	5	2	\N	3	\N	5
8	3	3	\N	\N	\N	5
9	4	3	\N	1	\N	5
10	4	3	\N	3	\N	5
11	5	3	\N	3	\N	5
18	3	2	\N	\N	\N	5
19	4	2	\N	\N	\N	5
20	5	2	\N	1	\N	5
21	5	2	\N	3	\N	5
22	3	3	\N	\N	\N	5
23	4	3	\N	\N	\N	5
24	5	3	\N	1	\N	5
25	5	3	\N	3	\N	5
26	3	2	\N	\N	\N	5
27	4	2	\N	\N	\N	5
28	5	2	\N	1	\N	5
29	5	2	\N	3	\N	5
30	3	3	\N	\N	\N	5
31	4	3	\N	\N	\N	5
32	5	3	\N	1	\N	5
33	5	3	\N	3	\N	5
34	3	2	\N	3	\N	5
35	4	2	\N	3	\N	5
36	5	2	\N	3	\N	5
37	7	2	\N	\N	\N	5
38	3	3	\N	3	\N	5
39	4	3	\N	3	\N	5
40	5	3	\N	3	\N	5
41	7	3	\N	\N	\N	5
42	3	2	\N	3	\N	5
43	4	2	\N	3	\N	5
44	5	2	\N	3	\N	5
45	7	2	\N	\N	\N	5
46	3	3	\N	3	\N	5
47	4	3	\N	3	\N	5
48	5	3	\N	3	\N	5
54	5	2	2	1	\N	3
55	5	2	1	1	\N	3
56	5	2	1	1	\N	3
57	5	2	\N	3	\N	3
58	5	3	2	1	\N	3
59	5	3	1	1	\N	3
60	5	3	1	1	\N	3
61	5	3	\N	3	\N	3
62	10	3	\N	\N	\N	4
63	21	3	\N	\N	\N	4
64	11	2	\N	\N	\N	4
65	10	2	\N	\N	\N	4
66	21	2	\N	\N	\N	4
67	11	2	\N	\N	\N	4
68	20	2	\N	\N	\N	4
69	13	2	\N	\N	\N	4
70	7	2	\N	\N	\N	4
71	20	3	\N	\N	\N	4
72	13	3	\N	\N	\N	4
73	7	2	\N	\N	\N	4
49	7	3	\N	\N	\N	5
\.


--
-- Data for Name: feed_emgsetup; Type: TABLE DATA; Schema: public; Owner: -
--

COPY feed_emgsetup (setup_ptr_id, preamplifier) FROM stdin;
59	Grass
3	Grass
28	Grass
30	Grass
57	Grass
34	Grass Model P511
32	Grass Model P511
\.


--
-- Data for Name: feed_emgunit; Type: TABLE DATA; Schema: public; Owner: -
--

COPY feed_emgunit (id, created_by_id, created_at, updated_at, label, controlled, deprecated) FROM stdin;
2	3	2009-08-11 01:00:00-04	2009-09-10 12:47:09.678285-04	volt	t	f
\.


--
-- Data for Name: feed_experiment; Type: TABLE DATA; Schema: public; Owner: -
--

COPY feed_experiment (id, created_by_id, created_at, updated_at, study_id, subject_id, accession, start, "end", bookkeeping, description, subj_devstage_id, subj_age, subj_weight, subj_tooth, subject_notes, impl_notes, title) FROM stdin;
7	8	2009-08-11 01:00:00-04	2009-08-11 11:44:44.574441-04	7	7		2009-08-11 12:43:57-04	2009-08-11 12:44:01-04		suckling data - LOTR pigs 	2	21.00000	5.00000				new Experiment - edit this
9	9	2009-08-24 00:00:00-04	2009-09-03 17:32:17.292275-04	8	8		2002-09-10 00:00:00-04	2002-09-10 23:59:59-04	Alpaca-Pe10Sep02H1	[# Experiment descr - Alpaca mastication EMGs  #] 	5	6.00000	\N	Full occlusion, evenly worn	Age: ~6 years		the only experiment
16	9	2009-08-26 00:00:00-04	2009-09-03 17:38:48.298881-04	11	10		2002-06-20 00:00:00-04	2002-06-20 23:59:59-04		[# descr of Exp 1 in Goat Mastication EMG study #] 	5	7.00000	74.00000	Full occlusion, evenly worn	Age\t~7 yrs\r\nWeight\t74 kg\r\njaw length: 23 cm from caudal border of angle to infradentale		Exp 1
31	7	2009-09-04 13:39:26.457019-04	2009-09-04 13:40:50.063453-04	13	12		2003-12-13 00:00:00-05	2003-12-13 00:00:00-05		Life Stage\tsubadult\r\nInstrumentation Notes\t\r\nStart Date\t12/3/2003\r\nEnd Date\t12/3/2003\r\nAge\tsubadult\r\nTooth Development\tM2s erupted\r\nWeight\t12.1 Kg\r\nAnimal Notes\tone of several experiments\r\n	4	\N	12.10000	M2s erupted	Tooth Development\tM2s erupted\r\nWeight\t12.1 Kg\r\nAnimal Notes\tone of several experiments\r\n		Experiment 1
32	8	2009-09-04 13:45:56.01425-04	2009-09-04 14:07:52.907237-04	14	13		2001-08-21 00:00:00-04	2001-01-21 23:59:59-05		[# ??? #] 	2	15.00000	5.00000		Infant, still suckling,\r\n15 days of age at start\r\n~5 kg\r\n	Sternothyrod and mylohyoid were patch electrodes, others needle/fine wire electrodes\r\n\r\n12 electrode channels\r\nchannel 14 = pressure transducer in teat (timing of suck)   [# not yet supported by DB #]\r\nchannel 15 = synchro with video camera (60 field/sec)       [# not yet supported by DB #]\r\n	the only experiment
3	6	2009-08-10 01:00:00-04	2009-09-10 12:00:48.183681-04	4	4		2001-01-16 01:00:00-05	2001-01-16 01:00:00-05	Lemur-BR01RN3	[# descr of Ring-tailed Lemur EMG - experiment #]	5	\N	\N	Fully erupted			the only experiment
8	6	2009-08-21 00:00:00-04	2009-09-10 12:12:59.193145-04	6	6		2001-08-10 00:00:00-04	\N		[#descr Experiment: in Treeshrew EMG #]	5	\N	\N	Fully erupted			the only experiment
4	6	2009-08-10 01:00:00-04	2009-09-10 12:13:38.559262-04	5	5		1999-12-20 01:00:00-05	1999-12-20 01:00:00-05		[#descr: Exp1 - Marmoset EMG#]\r\n	5	\N	\N	Fully erupted			the only experiment
\.


--
-- Data for Name: feed_illustration; Type: TABLE DATA; Schema: public; Owner: -
--

COPY feed_illustration (id, created_by_id, created_at, updated_at, picture, notes, subject_id, setup_id, experiment_id) FROM stdin;
3	6	2009-08-26 00:00:00-04	2009-08-26 09:31:51.86759-04	illustrations/Logot-lucida.png		\N	\N	8
\.


--
-- Data for Name: feed_muscle; Type: TABLE DATA; Schema: public; Owner: -
--

COPY feed_muscle (id, created_by_id, created_at, updated_at, label, controlled, deprecated) FROM stdin;
3	5	2009-08-10 01:00:00-04	2009-08-10 10:17:18.901005-04	Superficial Masseter	t	f
4	5	2009-08-10 01:00:00-04	2009-08-10 10:17:33.517377-04	Deep Masseter	t	f
5	5	2009-08-10 01:00:00-04	2009-08-10 10:17:46.351216-04	Temporalis	t	f
6	5	2009-08-10 01:00:00-04	2009-08-10 10:18:00.800607-04	Lateral Pterygoid	t	f
7	5	2009-08-10 01:00:00-04	2009-08-10 10:18:13.565405-04	Medial Pterygoid 	t	f
8	5	2009-08-10 01:00:00-04	2009-08-10 10:18:28.31143-04	Anterior Digastric 	t	f
9	5	2009-08-10 01:00:00-04	2009-08-10 11:59:41.192209-04	Posterior Digastric 	t	f
10	5	2009-08-10 01:00:00-04	2009-08-10 11:59:58.006489-04	Mylohyoid	t	f
11	5	2009-08-10 01:00:00-04	2009-08-10 12:00:07.365959-04	Geniohyoid	t	f
12	5	2009-08-10 01:00:00-04	2009-08-10 12:00:19.871976-04	Genioglossus	t	f
13	5	2009-08-10 01:00:00-04	2009-08-10 12:00:29.679401-04	Hyoglossus	t	f
14	5	2009-08-10 01:00:00-04	2009-08-10 12:00:37.632553-04	Styloglossus	t	f
15	5	2009-08-10 01:00:00-04	2009-08-10 12:00:45.911513-04	Palatoglossus	t	f
16	5	2009-08-10 01:00:00-04	2009-08-10 12:00:57.670901-04	Palatopharyngeus	t	f
17	5	2009-08-10 01:00:00-04	2009-08-10 12:01:18.646988-04	Superior Constrictor 	t	f
18	5	2009-08-10 01:00:00-04	2009-08-10 12:01:32.663259-04	Middle Constrictor 	t	f
19	5	2009-08-10 01:00:00-04	2009-08-10 12:01:42.966329-04	Inferior Constrictor 	t	f
20	5	2009-08-10 01:00:00-04	2009-08-10 12:01:51.4721-04	Omohyoid	t	f
21	5	2009-08-10 01:00:00-04	2009-08-10 12:02:16.854542-04	Sternohyoid	t	f
22	5	2009-08-10 01:00:00-04	2009-08-10 12:02:32.974528-04	Sternothyroid	t	f
23	5	2009-08-10 01:00:00-04	2009-08-10 12:02:47.030483-04	Thyrohyoid	t	f
\.


--
-- Data for Name: feed_restraint; Type: TABLE DATA; Schema: public; Owner: -
--

COPY feed_restraint (id, created_by_id, created_at, updated_at, label, controlled, deprecated) FROM stdin;
2	5	2009-08-10 01:00:00-04	2009-08-10 10:20:56.431563-04	None	t	f
3	5	2009-08-10 01:00:00-04	2009-08-10 10:21:04.856083-04	Chair	t	f
4	5	2009-08-10 01:00:00-04	2009-08-10 10:21:12.734155-04	Sling	t	f
5	5	2009-08-10 01:00:00-04	2009-08-10 10:21:27.790217-04	Hand-held	t	f
6	5	2009-08-10 01:00:00-04	2009-08-10 10:21:38.4863-04	Box	t	f
7	9	2009-08-24 00:00:00-04	2009-08-24 12:14:06.650741-04	Other	t	f
8	9	2009-08-26 00:00:00-04	2009-08-26 10:42:29.379421-04	Stall	t	f
9	8	2009-09-04 13:56:21.450719-04	2009-09-04 13:56:21.450719-04	Unknown	t	f
\.


--
-- Data for Name: feed_sensor; Type: TABLE DATA; Schema: public; Owner: -
--

COPY feed_sensor (id, created_by_id, created_at, updated_at, setup_id, name, notes) FROM stdin;
54	7	2009-09-04 13:59:56.705705-04	2009-09-10 10:34:39.991247-04	57	EMG1	\tElectrode Name\t DAT\r\n\tElectrode Type\tI\r\n\tElectrode Location\t1 cm superior to zyg arch\r\n\tImplantation Method\tneedle\r\n\tPosition Verification\tno\r\n
55	7	2009-09-04 14:06:21.523508-04	2009-09-10 10:48:11.827758-04	57	EMG2	\tElectrode Name\tSAT1\r\n\tElectrode Type\tI\r\n\tElectrode Location\t1 cm superior to zyg arch\r\n\tImplantation Method\tneedle\r\n\tPosition Verification\tno\r\n
62	8	2009-09-04 14:20:29.381649-04	2009-09-04 14:20:29.381649-04	59	EMG1	
16	\N	2009-08-12 01:00:00-04	2009-08-12 22:00:29.773986-04	3	channel 1	This is a test for chnale 1\r\n
63	8	2009-09-04 14:20:29.399717-04	2009-09-04 14:20:29.399717-04	59	EMG2	
64	8	2009-09-04 14:20:29.413908-04	2009-09-04 14:20:29.413908-04	59	EMG3	
4	\N	2009-08-12 01:00:00-04	2009-08-21 12:14:13.355184-04	3	LSM	
5	\N	2009-08-21 00:00:00-04	2009-08-21 12:14:13.383992-04	3	LDMA	
6	\N	2009-08-21 00:00:00-04	2009-08-21 12:14:13.406179-04	3	LDMP	
7	\N	2009-08-21 00:00:00-04	2009-08-21 12:14:13.426617-04	3	LPT	
8	\N	2009-08-21 00:00:00-04	2009-08-21 12:14:13.448556-04	3	RSM	
9	\N	2009-08-21 00:00:00-04	2009-08-21 12:14:13.469229-04	3	RDMA	
10	\N	2009-08-21 00:00:00-04	2009-08-21 12:14:13.489782-04	3	RDMP	
11	\N	2009-08-21 00:00:00-04	2009-08-21 12:14:13.510079-04	3	RPT	
18	\N	2009-08-21 00:00:00-04	2009-08-21 14:14:39.057723-04	28	LSM	
19	\N	2009-08-21 00:00:00-04	2009-08-21 14:23:02.966234-04	28	LDM	
20	\N	2009-08-21 00:00:00-04	2009-08-21 14:23:02.981867-04	28	LAT	
21	\N	2009-08-21 00:00:00-04	2009-08-21 14:23:02.995067-04	28	LPT	
22	\N	2009-08-21 00:00:00-04	2009-08-21 14:23:03.008788-04	28	RSM	
23	\N	2009-08-21 00:00:00-04	2009-08-21 14:23:03.022977-04	28	RDM	
24	\N	2009-08-21 00:00:00-04	2009-08-21 14:23:03.036812-04	28	RAT	
25	\N	2009-08-21 00:00:00-04	2009-08-21 14:23:52.736828-04	28	RPT	
26	\N	2009-08-21 00:00:00-04	2009-08-21 16:08:36.76822-04	30	LSM	
27	\N	2009-08-21 00:00:00-04	2009-08-21 16:13:51.209118-04	30	LDM	
28	\N	2009-08-21 00:00:00-04	2009-08-21 16:13:51.224526-04	30	LAT	
29	\N	2009-08-21 00:00:00-04	2009-08-21 16:13:51.238178-04	30	LPT	
30	\N	2009-08-21 00:00:00-04	2009-08-21 16:13:51.252005-04	30	RSM	
31	\N	2009-08-21 00:00:00-04	2009-08-21 16:13:51.265784-04	30	RDM	
32	\N	2009-08-21 00:00:00-04	2009-08-21 16:13:51.27951-04	30	RAT	
33	\N	2009-08-21 00:00:00-04	2009-08-21 16:13:51.293294-04	30	RPT	
65	8	2009-09-04 14:20:29.427863-04	2009-09-04 14:20:29.427863-04	59	EMG4	
66	8	2009-09-04 14:20:29.441869-04	2009-09-04 14:20:29.441869-04	59	EMG5	
67	8	2009-09-04 14:20:29.469553-04	2009-09-04 14:20:29.469553-04	59	EMG6	
68	8	2009-09-04 14:20:29.482296-04	2009-09-04 14:20:29.482296-04	59	EMG7	
69	8	2009-09-04 14:20:29.495547-04	2009-09-04 14:20:29.495547-04	59	EMG8	
70	8	2009-09-04 14:27:12.258385-04	2009-09-04 14:27:12.258385-04	59	EMG9	
71	8	2009-09-04 14:27:12.272358-04	2009-09-04 14:27:12.272358-04	59	EMG10	
72	8	2009-09-04 14:27:12.285108-04	2009-09-04 14:27:12.285108-04	59	EMG11	
73	8	2009-09-04 14:27:12.297597-04	2009-09-04 14:27:12.297597-04	59	EMG12	
56	7	2009-09-04 14:08:04.227844-04	2009-09-10 10:48:11.844264-04	57	EMG3	\tElectrode Name\tSAT2\r\n\tElectrode Type\tI\r\n\tElectrode Location\t1 cm superior to zyg arch\r\n\tImplantation Method\tneedle\r\n\tPosition Verification\tno\r\n
57	7	2009-09-04 14:08:04.24539-04	2009-09-10 10:48:11.974264-04	57	EMG4	\tElectrode Name\tPT\r\n\tElectrode Type\tI\r\n\tElectrode Side\tL\r\n\tElectrode Location\tposterior to ear\r\n\tImplantation Method\tneedle\r\n\tPosition Verification\tno\r\n
58	7	2009-09-04 14:15:05.461899-04	2009-09-10 10:51:07.404371-04	57	EMG5	\tElectrode Name\tDAT\r\n\tElectrode Type\tI\r\n\tElectrode Location\t1 cm superior to zyg arch\r\n\tImplantation Method\tneedle\r\n\tPosition Verification\tno
59	7	2009-09-04 14:15:05.481068-04	2009-09-10 10:51:07.421057-04	57	EMG6	\tElectrode Name\tSAT1\r\n\tElectrode Type\tI\r\n\tElectrode Location\t1 cm superior to zyg arch\r\n\tImplantation Method\tneedle\r\n\tPosition Verification\tno\r\n
60	7	2009-09-04 14:15:05.494296-04	2009-09-10 10:51:07.436322-04	57	EMG7	\tElectrode Name\tSAT2\r\n\tElectrode Type\tI\r\n\tElectrode Location\t1 cm superior to zyg arch\r\n\tImplantation Method\tneedle\r\n\tPosition Verification\tno\r\n
61	7	2009-09-04 14:15:05.506995-04	2009-09-10 10:51:07.48015-04	57	EMG8	\tElectrode Name\tPT\r\n\tElectrode Type\tI\r\n\tElectrode Location\tposterior to ear\r\n\tImplantation Method\tneedle\r\n\tPosition Verification\tno\r\n
34	9	2009-08-24 00:00:00-04	2009-09-10 11:32:20.512732-04	32	LSM	
35	9	2009-08-24 00:00:00-04	2009-09-10 11:34:12.74762-04	32	LDM	
36	9	2009-08-24 00:00:00-04	2009-09-10 11:34:12.763641-04	32	LPT	
37	9	2009-08-24 00:00:00-04	2009-09-10 11:34:12.778719-04	32	LMP	
38	9	2009-08-24 00:00:00-04	2009-09-10 11:34:12.794415-04	32	RSM	
39	9	2009-08-24 00:00:00-04	2009-09-10 11:34:12.809646-04	32	RDM	
40	9	2009-08-24 00:00:00-04	2009-09-10 11:34:12.824895-04	32	RPT	
41	9	2009-08-24 00:00:00-04	2009-09-10 11:34:12.839757-04	32	RMP	
42	9	2009-08-26 00:00:00-04	2009-09-10 11:45:08.384855-04	34	LSM	
43	9	2009-08-26 00:00:00-04	2009-09-10 11:45:08.401868-04	34	LDM	
44	9	2009-08-26 00:00:00-04	2009-09-10 11:45:08.417454-04	34	LPT	
45	9	2009-08-26 00:00:00-04	2009-09-10 11:45:08.432581-04	34	LMP	
46	9	2009-08-26 00:00:00-04	2009-09-10 11:45:08.447468-04	34	RSM	
47	9	2009-08-26 00:00:00-04	2009-09-10 11:45:08.46433-04	34	RDM	
48	9	2009-08-26 00:00:00-04	2009-09-10 11:45:08.479599-04	34	RPT	
49	9	2009-08-26 00:00:00-04	2009-09-10 11:45:08.495158-04	34	RMP	
\.


--
-- Data for Name: feed_session; Type: TABLE DATA; Schema: public; Owner: -
--

COPY feed_session (id, created_by_id, created_at, updated_at, experiment_id, accession, start, "end", "position", bookkeeping, subj_restraint_id, subj_anesthesia_sedation, subj_notes, title) FROM stdin;
7	8	2009-08-11 01:00:00-04	2009-08-11 11:55:12.719221-04	7		2009-08-11 12:54:46-04	2009-08-11 12:54:47-04	1		2			new Recording Session - edit this
12	9	2009-08-26 00:00:00-04	2009-09-03 17:40:16.539931-04	16		2002-06-20 06:00:00-04	2002-06-20 11:00:00-04	1		8			Sess 1
10	9	2009-08-24 00:00:00-04	2009-09-03 17:45:28.809117-04	9		2002-06-20 06:00:00-04	2002-06-20 11:00:00-04	1		8	0.305 ml butorphanol + 0.061 ml xylazine	At data entry, Start/end times were guessed from: \r\n        Start time\tMorning\r\n\tEnd Time\tLate morning	The only session
24	8	2009-09-04 14:05:51.516152-04	2009-09-04 14:36:43.781567-04	32		2001-08-21 21:03:00-04	\N	1		9			the only session
2	6	2009-08-10 01:00:00-04	2009-09-10 12:14:48.447585-04	3		2001-01-16 12:21:21-05	\N	1		3	Ketamine/Domitor		the only session
9	6	2009-08-21 00:00:00-04	2009-09-10 12:15:20.841091-04	8		2001-08-01 00:00:00-04	2001-08-01 00:00:00-04	1		4	Ketamine		the only session
3	6	2009-08-10 01:00:00-04	2009-09-10 12:15:41.342713-04	4		1999-12-20 01:00:00-05	\N	1		4	Ketamine		the only session
23	7	2009-09-04 13:45:40.694854-04	2009-09-10 13:34:19.175801-04	31		2003-12-03 09:00:00-05	2003-12-03 11:30:00-05	1		3	ketamine sub-cutaneous		recording session 1
\.


--
-- Data for Name: feed_setup; Type: TABLE DATA; Schema: public; Owner: -
--

COPY feed_setup (id, created_by_id, created_at, updated_at, experiment_id, technique_id, notes) FROM stdin;
8	\N	2009-08-14 01:00:00-04	2009-08-14 15:09:22.709449-04	4	5	\N
11	1	2009-08-14 01:00:00-04	2009-08-14 15:15:08.728625-04	4	1	\N
15	1	2009-08-14 01:00:00-04	2009-08-14 15:16:54.485425-04	4	1	\N
19	1	2009-08-14 01:00:00-04	2009-08-14 15:17:30.980606-04	4	5	\N
57	7	2009-09-04 13:40:50.158771-04	2009-09-10 10:51:07.382566-04	31	1	[#Electrode Names from the sample are not used in the table below, because they are not unique, such as SAT1 for both channel 1 and 6#]\r\n[# Also, there are 8 channels described in the metadata file NE12-3-03_VLRCP_Trial3.txt, but there are 11 columns in NE03VLRCP.dat, the last of which may be isn't an EMG.  #]\r\nElectrode Type\tI: [#interpreted as Indwelling Fine-Wire#]\r\n[# We have created "Chris Wall's filtering" value for the "EMG Filtering" column to represent this data from the sample: \r\n\tFiltering\tlow=100; high=3000\r\n\t60 Hz Notch Filter\tyes\r\n-- this should be changed to a more appropriate controlled value for the field.\r\n#]
3	6	2009-08-10 01:00:00-04	2009-08-21 12:14:13.268998-04	3	1	For all electrodes: \r\n\r\nImplantation Method:Needle\r\nPosition Verification: None\r\nPreamplifier Manufacturer: Grass\r\nAmplification:\t.\r\n60 Hz Notch Filter:\tYes\r\n
27	6	2009-08-21 00:00:00-04	2009-08-21 14:12:23.359757-04	4	1	\N
28	6	2009-08-21 00:00:00-04	2009-08-21 14:23:52.707886-04	4	1	Implantation Method:\tNeedle\r\nPosition Verification: \tNone\r\nAmplification:\t.\r\n60 Hz Notch Filter:\tYes
29	6	2009-08-21 00:00:00-04	2009-08-21 16:07:07.078965-04	8	1	\N
58	8	2009-09-04 14:07:52.924387-04	2009-09-04 14:07:52.924387-04	32	1	\N
30	6	2009-08-21 00:00:00-04	2009-08-21 16:15:44.654866-04	8	1	Implantation Method\tNeedle\r\nPosition Verification\tNone\r\nAmplification\t.\r\nFiltering\tBand Pass\r\n60 Hz Notch Filter\tYes
31	9	2009-08-24 00:00:00-04	2009-08-24 10:37:02.755393-04	9	1	\N
59	8	2009-09-04 14:07:52.926766-04	2009-09-04 14:27:12.228104-04	32	1	12 electrode channels\r\n\r\nME28 6sec.txt\r\nsurgically implanted\r\nTEAC DAT recorder\r\nverified post-mortem dissection\r\n\r\n[# in muscle notation, "rt" was understood "right", "lt" as "left".  What is "t" in "rt" and "lt"? #] 
33	9	2009-08-26 00:00:00-04	2009-08-26 10:07:00.326449-04	16	1	\N
34	9	2009-08-26 00:00:00-04	2009-09-10 11:46:02.24975-04	16	1	Common for all electrodes: \r\n\tImplantation Method\t: Percutaneous, Needle\r\n\tPosition Verification:\tNone\r\n\tPreamplifier Manufacturer: \tGrass\r\n\t60 Hz Notch Filter:\tYes\r\n
32	9	2009-08-24 00:00:00-04	2009-09-10 11:46:56.268292-04	9	1	Implantation Method\t"Percutaneous, Needle"\r\nPosition Verification\tNone\r\n60 Hz Notch Filter\tYes\r\n
56	7	2009-09-04 13:40:50.096236-04	2009-09-04 13:40:50.096236-04	31	1	\N
9	\N	2009-08-14 01:00:00-04	2009-08-14 15:09:50.8099-04	4	1	\N
10	\N	2009-08-14 01:00:00-04	2009-08-14 15:09:50.815307-04	4	5	\N
13	1	2009-08-14 01:00:00-04	2009-08-14 15:16:00.552569-04	4	1	\N
17	1	2009-08-14 01:00:00-04	2009-08-14 15:17:07.269419-04	4	5	\N
21	1	2009-08-14 01:00:00-04	2009-08-14 15:17:54.568447-04	4	1	\N
\.


--
-- Data for Name: feed_side; Type: TABLE DATA; Schema: public; Owner: -
--

COPY feed_side (id, created_by_id, created_at, updated_at, label, controlled, deprecated) FROM stdin;
2	5	2009-08-10 01:00:00-04	2009-08-10 10:19:52.952694-04	Left	t	f
3	5	2009-08-10 01:00:00-04	2009-08-10 10:20:00.967649-04	Right	t	f
4	5	2009-08-10 01:00:00-04	2009-08-10 10:20:10.989256-04	Midline	t	f
5	5	2009-08-10 01:00:00-04	2009-08-10 10:20:20.741221-04	Unknown	t	f
\.


--
-- Data for Name: feed_sonochannel; Type: TABLE DATA; Schema: public; Owner: -
--

COPY feed_sonochannel (channel_ptr_id, sono_unit_id, crystal1_id, crystal2_id) FROM stdin;
\.


--
-- Data for Name: feed_sonosensor; Type: TABLE DATA; Schema: public; Owner: -
--

COPY feed_sonosensor (sensor_ptr_id, muscle_id, side_id, axisdepth_id, axisap_id, axisdv_id) FROM stdin;
\.


--
-- Data for Name: feed_sonosetup; Type: TABLE DATA; Schema: public; Owner: -
--

COPY feed_sonosetup (setup_ptr_id, sonomicrometer) FROM stdin;
\.


--
-- Data for Name: feed_sonounit; Type: TABLE DATA; Schema: public; Owner: -
--

COPY feed_sonounit (id, created_by_id, created_at, updated_at, label, controlled, deprecated) FROM stdin;
1	6	2009-08-11 01:00:00-04	2009-08-11 12:36:40.76216-04	mm	t	f
\.


--
-- Data for Name: feed_study; Type: TABLE DATA; Schema: public; Owner: -
--

COPY feed_study (id, created_by_id, created_at, updated_at, accession, bookkeeping, start, "end", funding_agency, approval_secured, description, title) FROM stdin;
7	8	2009-08-10 01:00:00-04	2009-08-10 14:18:09.602351-04	24242424	ship pigs	2009-03-03 15:17:58-05	2009-03-24 01:00:00-04	NIH	JHU ACUC	EMG and SH sonomicrometrics 	infant pig suckling 1
4	6	2009-08-10 01:00:00-04	2009-08-21 11:25:44.999548-04		Lemur-BR01RN3	2001-01-09 00:00:00-05	2001-09-18 00:00:00-04		yes	Study of Ring-tailed Lemur EMG	Ring-tailed Lemur EMG
5	6	2009-08-10 01:00:00-04	2009-08-21 15:08:11.056259-04		Marmoset-Mi99A2	1999-11-11 00:00:00-05	2002-10-18 00:00:00-04		yes	Study of Marmoset EMG	Marmoset EMG
11	9	2009-08-26 00:00:00-04	2009-08-26 12:27:49.905295-04		Study of trial DO20June02H5	2002-01-01 00:00:00-05	2004-12-31 00:00:00-05	National Science Foundation	yes	[# Descr for Goat mastication EMGs study #]	Goat mastication EMGs
8	9	2009-08-21 00:00:00-04	2009-08-26 12:29:07.624126-04		Study of  trial Pe10Sep02H1	2001-01-01 00:00:00-05	2004-12-31 00:00:00-05	National Science Foundation	yes	[#Descr for Study: Alpaca mastication EMGs #]	Alpaca mastication EMGs
6	6	2009-08-10 01:00:00-04	2009-08-26 16:36:51.497301-04		Treeshrew-DB01CR1	2001-07-26 01:00:00-04	2002-01-16 01:00:00-05		yes	Study of Treeshrew EMG	Treeshrew EMG
13	7	2009-09-04 13:31:47.569934-04	2009-09-04 13:31:47.569934-04			2001-01-01 00:00:00-05	2003-12-31 00:00:00-05		yes	chewing	Superficial Temporalis Study
14	8	2009-09-04 13:34:47.907102-04	2009-09-04 13:34:47.907102-04			2001-08-01 12:00:00-04	2001-08-31 12:00:00-04			EMG study of infant pig, including EMG and videofluroscopy	Infant Pig Suckling and Swallowing
\.


--
-- Data for Name: feed_studyprivate; Type: TABLE DATA; Schema: public; Owner: -
--

COPY feed_studyprivate (id, created_by_id, created_at, updated_at, study_id, pi, organization, lab, funding, approval, notes) FROM stdin;
4	\N	2009-08-10 01:00:00-04	2009-08-10 10:50:28.864081-04	4	Chris Vinyard	BAA-Duke University	Hylander		DU-IACUC	
7	\N	2009-08-10 01:00:00-04	2009-08-10 14:18:09.606624-04	7	RZ German	JHU	German	NIH 		
5	\N	2009-08-10 01:00:00-04	2009-08-21 14:07:32.334549-04	5	Chris Vinyard	BAA-Duke University	Hylander		DU-IACUC	Email\tcvinyard@neoucom.edu\r\nWebpage\thttp://www.neoucom.edu/audience/about/departments/anatneuro/
6	\N	2009-08-10 01:00:00-04	2009-08-21 14:37:03.287852-04	6	Chris Vinyard	BAA-Duke University	Hylander		DU-IACUC	Email\tcvinyard@neoucom.edu\r\nWebpage\thttp://www.neoucom.edu/audience/about/departments/anatneuro/faculty/ChrisVinyard/
8	\N	2009-08-21 00:00:00-04	2009-08-21 14:44:08.345307-04	8	Susan H. Williams	Duke University	William Hylander	BCS-0241652 and SBR-138565	Duke IACUC	Email\twillias7@ohio.edu\r\nWebpage\thttp://www.oucom.ohiou.edu/dbms-williams/
11	9	2009-08-26 00:00:00-04	2009-08-26 09:50:00.776181-04	11	Susan H. Williams	Duke University	SH Williams	BCS-0241652 and SBR-138565	Duke IACUC	\tEmail\twillias7@ohio.edu\r\n\tWebpage\thttp://www.oucom.ohiou.edu/dbms-williams/\r\n
13	7	2009-09-04 13:31:47.627769-04	2009-09-04 13:31:47.627769-04	13	Christine E. Wall	Duke University	Wall/Hylander	NSF	IACUC	
14	8	2009-09-04 13:34:47.911336-04	2009-09-04 13:34:47.911336-04	14	Rebecca Z. German	Museum of Comparative Zoology, Harvard University				rz.german@jhmi.edu
\.


--
-- Data for Name: feed_subject; Type: TABLE DATA; Schema: public; Owner: -
--

COPY feed_subject (id, created_by_id, created_at, updated_at, study_id, taxon_id, name, breed, sex, source, notes) FROM stdin;
4	6	2009-08-10 01:00:00-04	2009-08-10 11:08:48.369394-04	4	2	Brennus		M	Duke University Primate Center	
5	6	2009-08-10 01:00:00-04	2009-08-10 11:11:39.040718-04	5	3	Mickey		M	Duke University	
7	8	2009-08-11 01:00:00-04	2009-08-11 11:43:35.03125-04	7	4	gandalf		F		
8	9	2009-08-11 01:00:00-04	2009-08-24 10:23:28.577507-04	8	5	Perla	huacaya	F	Ohio State University	
10	9	2009-08-26 00:00:00-04	2009-08-26 10:05:35.353413-04	11	7	Domingo	Boer/Nubian Cross	M	Duke University	
6	6	2009-08-10 01:00:00-04	2009-08-26 16:36:51.508234-04	6	4	Doughboy		\N	Duke University	
13	8	2009-09-04 13:34:47.914791-04	2009-09-04 13:46:51.999188-04	14	6	Meatless		F		DOB 8/6\r\n22 days old   [# this contradicts to "15 days" in the Experiment #]\r\n
12	7	2009-09-04 13:33:55.686614-04	2009-09-09 12:02:44.083752-04	13	8	Nefertiti 2-11	East Africa?	F	Duke Vivarium	excellent subject\r\n
\.


--
-- Data for Name: feed_taxon; Type: TABLE DATA; Schema: public; Owner: -
--

COPY feed_taxon (id, created_by_id, created_at, updated_at, label, controlled, deprecated, genus, species, common_name) FROM stdin;
5	3	2009-08-10 01:00:00-04	2009-08-10 10:14:03.573334-04	Alpaca	t	f	Lama	pacos	Alpaca
4	3	2009-08-10 01:00:00-04	2009-08-13 10:32:01.691275-04	Belanger's Treeshrew	t	f	Tupaia	belangeri	Belanger's Treeshrew
6	8	2009-08-11 01:00:00-04	2009-08-21 11:14:56.756124-04	Sus scrofa	t	f	Sus	scrofa	pig
3	3	2009-08-10 01:00:00-04	2009-08-21 11:15:50.892101-04	common marmoset	t	f	Callithrix	jacchus	common marmoset
2	3	2009-08-10 01:00:00-04	2009-08-21 11:18:37.601725-04	Lemur catta	t	f	Lemur	catta	ring-tailed lemur
7	9	2009-08-26 00:00:00-04	2009-08-26 09:49:15.388986-04	Goat	t	f	Capra	hircus	Goat
8	7	2009-09-04 13:32:49.819178-04	2009-09-04 13:32:49.819178-04	Papio anubis	t	f	Papio	anubis	baboon
\.


--
-- Data for Name: feed_technique; Type: TABLE DATA; Schema: public; Owner: -
--

COPY feed_technique (id, created_by_id, created_at, updated_at, label, controlled, deprecated) FROM stdin;
1	1	2009-08-04 01:00:00-04	2009-08-06 14:40:02.875591-04	EMG	t	f
5	\N	2009-08-05 01:00:00-04	2009-08-06 14:40:22.788628-04	Sono	t	f
8	5	2009-08-06 01:00:00-04	2009-08-06 14:42:00.800373-04	Bone strain	t	f
9	5	2009-08-06 01:00:00-04	2009-08-06 14:44:12.007087-04	Bite force	t	f
10	5	2009-08-06 01:00:00-04	2009-08-06 14:44:47.701593-04	Pressure	t	f
11	5	2009-08-06 01:00:00-04	2009-08-06 14:45:01.499598-04	Kinematics	t	f
\.


--
-- Data for Name: feed_trial; Type: TABLE DATA; Schema: public; Owner: -
--

COPY feed_trial (id, created_by_id, created_at, updated_at, session_id, accession, "position", start, "end", claimed_duration, bookkeeping, subj_treatment, subj_notes, food_type, food_size, food_property, behavior_primary_id, behavior_secondary, behavior_notes, waveform_picture, title) FROM stdin;
6	9	2009-08-26 00:00:00-04	2009-08-26 10:47:09.052501-04	12		1	\N	\N	36.4900	DO20June02H5	None		hay	NA	tough	3	Ingestion	chewing sides from beginning: 7 left chews, 29 right chews, 9 left chews, 12 right chews; 4 possible bouts of ingestion visible.\r\n\r\n\tChewing Side:\tBoth\r\n\tNumber of Chews:\t57\r\n		new Trial - edit this
5	9	2009-08-24 00:00:00-04	2009-09-03 17:44:46.299347-04	10		1	\N	\N	40.9900	Pe10Sep02H1			hay		tough	3	None	Chewing Side\tLeft\r\nNumber of Chews\t44\r\n		The only trial
10	8	2009-09-04 14:36:43.804913-04	2009-09-04 14:40:44.692369-04	24		1	\N	\N	6.0000		* experimental treatment: intact	* duration: ~30 sec, 6 seconds in dataset\r\n\r\n* material properties of food: liquid\r\n\r\n	milk		liquid	4	Swallowing	* level of satiation: full at the end\r\n		T28
9	7	2009-09-04 14:26:58.287607-04	2009-09-10 10:56:25.740475-04	23		3	\N	\N	\N	tape footage 255-418, Tape 97			cherry pits	approx. 10 mm length		10	probably intercalated swallows	\t\tchannel 5 is noisy\r\nChewing Side\tleft and right\r\n\tNumber of Chews\t60\r\n\tAnnotations\t\r\n\tOriginal Filename\tNE03VLRCP.dat\r\n\tGraphic Display Available\t\r\n\r\n\r\n[#not sure where to put this notes. maybe a trial notes field is needed #]		Trial 3
2	6	2009-08-10 01:00:00-04	2009-09-10 12:16:12.116066-04	2		1	2001-01-16 12:27:46-05	2001-01-16 12:28:02-05	16.0000	BR01RN3			Raisin			3	Ingestion, swallowing	Chewing on both sides. \r\nNumber of Chews: 26. 		the only trial
3	6	2009-08-21 00:00:00-04	2009-09-10 12:16:59.177855-04	3		1	1999-12-20 00:00:00-05	\N	26.0000	Mi99A2			Apple			3	Ingestion, Swallowing	Chewing Side:\tBoth\r\nNumber of Chews:\t~37\r\n		the only trial
4	6	2009-08-21 00:00:00-04	2009-09-10 12:17:34.950346-04	9		1	2001-08-01 00:00:00-04	2001-08-01 00:00:00-04	9.3000	DB01CR1			Cricket			3	Ingestion, Swallowing	Chewing Side\tBoth\r\nNumber of Chews\t~30\r\n		the only trial
\.


--
-- Data for Name: south_migrationhistory; Type: TABLE DATA; Schema: public; Owner: -
--

COPY south_migrationhistory (id, app_name, migration, applied) FROM stdin;
1	feed	0001_initial	2009-09-01 19:09:45.589994-04
2	feed	0002_add_container_names	2009-09-03 21:00:05.338794-04
3	feed	0003_names2titles_add_null_title	2009-09-03 21:00:05.540114-04
4	feed	0004_name2title_copy_data	2009-09-03 21:00:05.849547-04
5	feed	0005_name2title_drop_name	2009-09-03 21:00:06.130933-04
6	feed	0006_add_amplification_field	2009-09-04 19:49:52.153133-04
7	feed	0007_link_electrode_to_sensor_and_channel	2009-09-08 20:22:34.57346-04
8	feed	0008_link_electrode_datamigr	2009-09-08 20:22:35.513809-04
9	feed	0009_make_amplification_blankable	2009-09-08 21:43:20.063012-04
\.


--
-- Name: auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions_group_id_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_key UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_message_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY auth_message
    ADD CONSTRAINT auth_message_pkey PRIMARY KEY (id);


--
-- Name: auth_permission_content_type_id_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_key UNIQUE (content_type_id, codename);


--
-- Name: auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_key UNIQUE (user_id, group_id);


--
-- Name: auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_key UNIQUE (user_id, permission_id);


--
-- Name: auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type_app_label_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_app_label_key UNIQUE (app_label, model);


--
-- Name: django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: django_site_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY django_site
    ADD CONSTRAINT django_site_pkey PRIMARY KEY (id);


--
-- Name: feed_anteriorposterioraxis_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY feed_anteriorposterioraxis
    ADD CONSTRAINT feed_anteriorposterioraxis_pkey PRIMARY KEY (id);


--
-- Name: feed_behavior_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY feed_behavior
    ADD CONSTRAINT feed_behavior_pkey PRIMARY KEY (id);


--
-- Name: feed_channel_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY feed_channel
    ADD CONSTRAINT feed_channel_pkey PRIMARY KEY (id);


--
-- Name: feed_channellineup_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY feed_channellineup
    ADD CONSTRAINT feed_channellineup_pkey PRIMARY KEY (id);


--
-- Name: feed_depthaxis_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY feed_depthaxis
    ADD CONSTRAINT feed_depthaxis_pkey PRIMARY KEY (id);


--
-- Name: feed_developmentstage_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY feed_developmentstage
    ADD CONSTRAINT feed_developmentstage_pkey PRIMARY KEY (id);


--
-- Name: feed_dorsalventralaxis_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY feed_dorsalventralaxis
    ADD CONSTRAINT feed_dorsalventralaxis_pkey PRIMARY KEY (id);


--
-- Name: feed_eletrodetype_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY feed_electrodetype
    ADD CONSTRAINT feed_eletrodetype_pkey PRIMARY KEY (id);


--
-- Name: feed_emgchannel_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY feed_emgchannel
    ADD CONSTRAINT feed_emgchannel_pkey PRIMARY KEY (channel_ptr_id);


--
-- Name: feed_emgelectrode_channel_id_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY feed_emgelectrode
    ADD CONSTRAINT feed_emgelectrode_channel_id_key UNIQUE (channel_id);


--
-- Name: feed_emgelectrode_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY feed_emgelectrode
    ADD CONSTRAINT feed_emgelectrode_pkey PRIMARY KEY (id);


--
-- Name: feed_emgelectrode_sensor_id_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY feed_emgelectrode
    ADD CONSTRAINT feed_emgelectrode_sensor_id_key UNIQUE (sensor_id);


--
-- Name: feed_emgfiltering_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY feed_emgfiltering
    ADD CONSTRAINT feed_emgfiltering_pkey PRIMARY KEY (id);


--
-- Name: feed_emgsensor_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY feed_emgsensor
    ADD CONSTRAINT feed_emgsensor_pkey PRIMARY KEY (sensor_ptr_id);


--
-- Name: feed_emgsetup_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY feed_emgsetup
    ADD CONSTRAINT feed_emgsetup_pkey PRIMARY KEY (setup_ptr_id);


--
-- Name: feed_emgunit_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY feed_emgunit
    ADD CONSTRAINT feed_emgunit_pkey PRIMARY KEY (id);


--
-- Name: feed_experiment_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY feed_experiment
    ADD CONSTRAINT feed_experiment_pkey PRIMARY KEY (id);


--
-- Name: feed_illustration_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY feed_illustration
    ADD CONSTRAINT feed_illustration_pkey PRIMARY KEY (id);


--
-- Name: feed_muscle_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY feed_muscle
    ADD CONSTRAINT feed_muscle_pkey PRIMARY KEY (id);


--
-- Name: feed_restraint_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY feed_restraint
    ADD CONSTRAINT feed_restraint_pkey PRIMARY KEY (id);


--
-- Name: feed_sensor_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY feed_sensor
    ADD CONSTRAINT feed_sensor_pkey PRIMARY KEY (id);


--
-- Name: feed_session_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY feed_session
    ADD CONSTRAINT feed_session_pkey PRIMARY KEY (id);


--
-- Name: feed_setup_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY feed_setup
    ADD CONSTRAINT feed_setup_pkey PRIMARY KEY (id);


--
-- Name: feed_side_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY feed_side
    ADD CONSTRAINT feed_side_pkey PRIMARY KEY (id);


--
-- Name: feed_sonochannel_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY feed_sonochannel
    ADD CONSTRAINT feed_sonochannel_pkey PRIMARY KEY (channel_ptr_id);


--
-- Name: feed_sonosensor_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY feed_sonosensor
    ADD CONSTRAINT feed_sonosensor_pkey PRIMARY KEY (sensor_ptr_id);


--
-- Name: feed_sonosetup_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY feed_sonosetup
    ADD CONSTRAINT feed_sonosetup_pkey PRIMARY KEY (setup_ptr_id);


--
-- Name: feed_sonounit_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY feed_sonounit
    ADD CONSTRAINT feed_sonounit_pkey PRIMARY KEY (id);


--
-- Name: feed_study_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY feed_study
    ADD CONSTRAINT feed_study_pkey PRIMARY KEY (id);


--
-- Name: feed_studyprivate_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY feed_studyprivate
    ADD CONSTRAINT feed_studyprivate_pkey PRIMARY KEY (id);


--
-- Name: feed_subject_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY feed_subject
    ADD CONSTRAINT feed_subject_pkey PRIMARY KEY (id);


--
-- Name: feed_taxon_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY feed_taxon
    ADD CONSTRAINT feed_taxon_pkey PRIMARY KEY (id);


--
-- Name: feed_technique_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY feed_technique
    ADD CONSTRAINT feed_technique_pkey PRIMARY KEY (id);


--
-- Name: feed_trial_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY feed_trial
    ADD CONSTRAINT feed_trial_pkey PRIMARY KEY (id);


--
-- Name: south_migrationhistory_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY south_migrationhistory
    ADD CONSTRAINT south_migrationhistory_pkey PRIMARY KEY (id);


--
-- Name: auth_message_user_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX auth_message_user_id ON auth_message USING btree (user_id);


--
-- Name: auth_permission_content_type_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX auth_permission_content_type_id ON auth_permission USING btree (content_type_id);


--
-- Name: django_admin_log_content_type_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX django_admin_log_content_type_id ON django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX django_admin_log_user_id ON django_admin_log USING btree (user_id);


--
-- Name: feed_anteriorposterioraxis_created_by_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_anteriorposterioraxis_created_by_id ON feed_anteriorposterioraxis USING btree (created_by_id);


--
-- Name: feed_behavior_created_by_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_behavior_created_by_id ON feed_behavior USING btree (created_by_id);


--
-- Name: feed_channel_created_by_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_channel_created_by_id ON feed_channel USING btree (created_by_id);


--
-- Name: feed_channel_setup_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_channel_setup_id ON feed_channel USING btree (setup_id);


--
-- Name: feed_channellineup_channel_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_channellineup_channel_id ON feed_channellineup USING btree (channel_id);


--
-- Name: feed_channellineup_created_by_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_channellineup_created_by_id ON feed_channellineup USING btree (created_by_id);


--
-- Name: feed_channellineup_session_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_channellineup_session_id ON feed_channellineup USING btree (session_id);


--
-- Name: feed_depthaxis_created_by_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_depthaxis_created_by_id ON feed_depthaxis USING btree (created_by_id);


--
-- Name: feed_developmentstage_created_by_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_developmentstage_created_by_id ON feed_developmentstage USING btree (created_by_id);


--
-- Name: feed_dorsalventralaxis_created_by_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_dorsalventralaxis_created_by_id ON feed_dorsalventralaxis USING btree (created_by_id);


--
-- Name: feed_eletrodetype_created_by_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_eletrodetype_created_by_id ON feed_electrodetype USING btree (created_by_id);


--
-- Name: feed_emgchannel_emg_filtering_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_emgchannel_emg_filtering_id ON feed_emgchannel USING btree (emg_filtering_id);


--
-- Name: feed_emgchannel_emg_unit_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_emgchannel_emg_unit_id ON feed_emgchannel USING btree (emg_unit_id);


--
-- Name: feed_emgchannel_sensor_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_emgchannel_sensor_id ON feed_emgchannel USING btree (sensor_id);


--
-- Name: feed_emgelectrode_axisap_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_emgelectrode_axisap_id ON feed_emgelectrode USING btree (axisap_id);


--
-- Name: feed_emgelectrode_axisdepth_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_emgelectrode_axisdepth_id ON feed_emgelectrode USING btree (axisdepth_id);


--
-- Name: feed_emgelectrode_axisdv_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_emgelectrode_axisdv_id ON feed_emgelectrode USING btree (axisdv_id);


--
-- Name: feed_emgelectrode_created_by_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_emgelectrode_created_by_id ON feed_emgelectrode USING btree (created_by_id);


--
-- Name: feed_emgelectrode_eletrode_type_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_emgelectrode_eletrode_type_id ON feed_emgelectrode USING btree (electrode_type_id);


--
-- Name: feed_emgelectrode_emg_filtering_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_emgelectrode_emg_filtering_id ON feed_emgelectrode USING btree (emg_filtering_id);


--
-- Name: feed_emgelectrode_emg_unit_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_emgelectrode_emg_unit_id ON feed_emgelectrode USING btree (emg_unit_id);


--
-- Name: feed_emgelectrode_muscle_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_emgelectrode_muscle_id ON feed_emgelectrode USING btree (muscle_id);


--
-- Name: feed_emgelectrode_setup_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_emgelectrode_setup_id ON feed_emgelectrode USING btree (setup_id);


--
-- Name: feed_emgelectrode_side_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_emgelectrode_side_id ON feed_emgelectrode USING btree (side_id);


--
-- Name: feed_emgfiltering_created_by_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_emgfiltering_created_by_id ON feed_emgfiltering USING btree (created_by_id);


--
-- Name: feed_emgsensor_axisap_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_emgsensor_axisap_id ON feed_emgsensor USING btree (axisap_id);


--
-- Name: feed_emgsensor_axisdepth_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_emgsensor_axisdepth_id ON feed_emgsensor USING btree (axisdepth_id);


--
-- Name: feed_emgsensor_axisdv_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_emgsensor_axisdv_id ON feed_emgsensor USING btree (axisdv_id);


--
-- Name: feed_emgsensor_eletrode_type_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_emgsensor_eletrode_type_id ON feed_emgsensor USING btree (electrode_type_id);


--
-- Name: feed_emgsensor_muscle_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_emgsensor_muscle_id ON feed_emgsensor USING btree (muscle_id);


--
-- Name: feed_emgsensor_side_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_emgsensor_side_id ON feed_emgsensor USING btree (side_id);


--
-- Name: feed_emgunit_created_by_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_emgunit_created_by_id ON feed_emgunit USING btree (created_by_id);


--
-- Name: feed_experiment_created_by_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_experiment_created_by_id ON feed_experiment USING btree (created_by_id);


--
-- Name: feed_experiment_study_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_experiment_study_id ON feed_experiment USING btree (study_id);


--
-- Name: feed_experiment_subj_devstage_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_experiment_subj_devstage_id ON feed_experiment USING btree (subj_devstage_id);


--
-- Name: feed_experiment_subject_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_experiment_subject_id ON feed_experiment USING btree (subject_id);


--
-- Name: feed_illustration_created_by_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_illustration_created_by_id ON feed_illustration USING btree (created_by_id);


--
-- Name: feed_illustration_experiment_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_illustration_experiment_id ON feed_illustration USING btree (experiment_id);


--
-- Name: feed_illustration_setup_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_illustration_setup_id ON feed_illustration USING btree (setup_id);


--
-- Name: feed_illustration_subject_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_illustration_subject_id ON feed_illustration USING btree (subject_id);


--
-- Name: feed_muscle_created_by_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_muscle_created_by_id ON feed_muscle USING btree (created_by_id);


--
-- Name: feed_restraint_created_by_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_restraint_created_by_id ON feed_restraint USING btree (created_by_id);


--
-- Name: feed_sensor_created_by_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_sensor_created_by_id ON feed_sensor USING btree (created_by_id);


--
-- Name: feed_sensor_setup_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_sensor_setup_id ON feed_sensor USING btree (setup_id);


--
-- Name: feed_session_created_by_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_session_created_by_id ON feed_session USING btree (created_by_id);


--
-- Name: feed_session_experiment_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_session_experiment_id ON feed_session USING btree (experiment_id);


--
-- Name: feed_session_subj_restraint_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_session_subj_restraint_id ON feed_session USING btree (subj_restraint_id);


--
-- Name: feed_setup_created_by_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_setup_created_by_id ON feed_setup USING btree (created_by_id);


--
-- Name: feed_setup_experiment_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_setup_experiment_id ON feed_setup USING btree (experiment_id);


--
-- Name: feed_setup_technique_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_setup_technique_id ON feed_setup USING btree (technique_id);


--
-- Name: feed_side_created_by_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_side_created_by_id ON feed_side USING btree (created_by_id);


--
-- Name: feed_sonochannel_crystal1_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_sonochannel_crystal1_id ON feed_sonochannel USING btree (crystal1_id);


--
-- Name: feed_sonochannel_crystal2_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_sonochannel_crystal2_id ON feed_sonochannel USING btree (crystal2_id);


--
-- Name: feed_sonochannel_sono_unit_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_sonochannel_sono_unit_id ON feed_sonochannel USING btree (sono_unit_id);


--
-- Name: feed_sonosensor_axisap_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_sonosensor_axisap_id ON feed_sonosensor USING btree (axisap_id);


--
-- Name: feed_sonosensor_axisdepth_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_sonosensor_axisdepth_id ON feed_sonosensor USING btree (axisdepth_id);


--
-- Name: feed_sonosensor_axisdv_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_sonosensor_axisdv_id ON feed_sonosensor USING btree (axisdv_id);


--
-- Name: feed_sonosensor_muscle_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_sonosensor_muscle_id ON feed_sonosensor USING btree (muscle_id);


--
-- Name: feed_sonosensor_side_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_sonosensor_side_id ON feed_sonosensor USING btree (side_id);


--
-- Name: feed_sonounit_created_by_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_sonounit_created_by_id ON feed_sonounit USING btree (created_by_id);


--
-- Name: feed_study_created_by_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_study_created_by_id ON feed_study USING btree (created_by_id);


--
-- Name: feed_studyprivate_created_by_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_studyprivate_created_by_id ON feed_studyprivate USING btree (created_by_id);


--
-- Name: feed_studyprivate_study_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_studyprivate_study_id ON feed_studyprivate USING btree (study_id);


--
-- Name: feed_subject_created_by_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_subject_created_by_id ON feed_subject USING btree (created_by_id);


--
-- Name: feed_subject_study_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_subject_study_id ON feed_subject USING btree (study_id);


--
-- Name: feed_subject_taxon_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_subject_taxon_id ON feed_subject USING btree (taxon_id);


--
-- Name: feed_taxon_created_by_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_taxon_created_by_id ON feed_taxon USING btree (created_by_id);


--
-- Name: feed_technique_created_by_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_technique_created_by_id ON feed_technique USING btree (created_by_id);


--
-- Name: feed_trial_behavior_primary_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_trial_behavior_primary_id ON feed_trial USING btree (behavior_primary_id);


--
-- Name: feed_trial_created_by_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_trial_created_by_id ON feed_trial USING btree (created_by_id);


--
-- Name: feed_trial_session_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX feed_trial_session_id ON feed_trial USING btree (session_id);


--
-- Name: auth_group_permissions_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_fkey FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_message_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY auth_message
    ADD CONSTRAINT auth_message_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_fkey FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: channel_id_refs_channel_ptr_id_4f00a7dd; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_emgelectrode
    ADD CONSTRAINT channel_id_refs_channel_ptr_id_4f00a7dd FOREIGN KEY (channel_id) REFERENCES feed_emgchannel(channel_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: content_type_id_refs_id_728de91f; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT content_type_id_refs_id_728de91f FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log_content_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_fkey FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_anteriorposterioraxis_created_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_anteriorposterioraxis
    ADD CONSTRAINT feed_anteriorposterioraxis_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_behavior_created_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_behavior
    ADD CONSTRAINT feed_behavior_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_channel_created_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_channel
    ADD CONSTRAINT feed_channel_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_channel_setup_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_channel
    ADD CONSTRAINT feed_channel_setup_id_fkey FOREIGN KEY (setup_id) REFERENCES feed_setup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_channellineup_channel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_channellineup
    ADD CONSTRAINT feed_channellineup_channel_id_fkey FOREIGN KEY (channel_id) REFERENCES feed_channel(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_channellineup_created_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_channellineup
    ADD CONSTRAINT feed_channellineup_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_channellineup_session_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_channellineup
    ADD CONSTRAINT feed_channellineup_session_id_fkey FOREIGN KEY (session_id) REFERENCES feed_session(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_depthaxis_created_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_depthaxis
    ADD CONSTRAINT feed_depthaxis_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_developmentstage_created_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_developmentstage
    ADD CONSTRAINT feed_developmentstage_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_dorsalventralaxis_created_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_dorsalventralaxis
    ADD CONSTRAINT feed_dorsalventralaxis_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_eletrodetype_created_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_electrodetype
    ADD CONSTRAINT feed_eletrodetype_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_emgchannel_channel_ptr_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_emgchannel
    ADD CONSTRAINT feed_emgchannel_channel_ptr_id_fkey FOREIGN KEY (channel_ptr_id) REFERENCES feed_channel(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_emgchannel_emg_filtering_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_emgchannel
    ADD CONSTRAINT feed_emgchannel_emg_filtering_id_fkey FOREIGN KEY (emg_filtering_id) REFERENCES feed_emgfiltering(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_emgchannel_emg_unit_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_emgchannel
    ADD CONSTRAINT feed_emgchannel_emg_unit_id_fkey FOREIGN KEY (emg_unit_id) REFERENCES feed_emgunit(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_emgchannel_sensor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_emgchannel
    ADD CONSTRAINT feed_emgchannel_sensor_id_fkey FOREIGN KEY (sensor_id) REFERENCES feed_emgsensor(sensor_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_emgelectrode_axisap_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_emgelectrode
    ADD CONSTRAINT feed_emgelectrode_axisap_id_fkey FOREIGN KEY (axisap_id) REFERENCES feed_anteriorposterioraxis(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_emgelectrode_axisdepth_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_emgelectrode
    ADD CONSTRAINT feed_emgelectrode_axisdepth_id_fkey FOREIGN KEY (axisdepth_id) REFERENCES feed_depthaxis(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_emgelectrode_axisdv_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_emgelectrode
    ADD CONSTRAINT feed_emgelectrode_axisdv_id_fkey FOREIGN KEY (axisdv_id) REFERENCES feed_dorsalventralaxis(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_emgelectrode_created_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_emgelectrode
    ADD CONSTRAINT feed_emgelectrode_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_emgelectrode_eletrode_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_emgelectrode
    ADD CONSTRAINT feed_emgelectrode_eletrode_type_id_fkey FOREIGN KEY (electrode_type_id) REFERENCES feed_electrodetype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_emgelectrode_emg_filtering_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_emgelectrode
    ADD CONSTRAINT feed_emgelectrode_emg_filtering_id_fkey FOREIGN KEY (emg_filtering_id) REFERENCES feed_emgfiltering(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_emgelectrode_emg_unit_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_emgelectrode
    ADD CONSTRAINT feed_emgelectrode_emg_unit_id_fkey FOREIGN KEY (emg_unit_id) REFERENCES feed_emgunit(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_emgelectrode_muscle_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_emgelectrode
    ADD CONSTRAINT feed_emgelectrode_muscle_id_fkey FOREIGN KEY (muscle_id) REFERENCES feed_muscle(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_emgelectrode_setup_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_emgelectrode
    ADD CONSTRAINT feed_emgelectrode_setup_id_fkey FOREIGN KEY (setup_id) REFERENCES feed_setup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_emgelectrode_side_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_emgelectrode
    ADD CONSTRAINT feed_emgelectrode_side_id_fkey FOREIGN KEY (side_id) REFERENCES feed_side(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_emgfiltering_created_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_emgfiltering
    ADD CONSTRAINT feed_emgfiltering_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_emgsensor_axisap_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_emgsensor
    ADD CONSTRAINT feed_emgsensor_axisap_id_fkey FOREIGN KEY (axisap_id) REFERENCES feed_anteriorposterioraxis(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_emgsensor_axisdepth_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_emgsensor
    ADD CONSTRAINT feed_emgsensor_axisdepth_id_fkey FOREIGN KEY (axisdepth_id) REFERENCES feed_depthaxis(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_emgsensor_axisdv_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_emgsensor
    ADD CONSTRAINT feed_emgsensor_axisdv_id_fkey FOREIGN KEY (axisdv_id) REFERENCES feed_dorsalventralaxis(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_emgsensor_eletrode_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_emgsensor
    ADD CONSTRAINT feed_emgsensor_eletrode_type_id_fkey FOREIGN KEY (electrode_type_id) REFERENCES feed_electrodetype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_emgsensor_muscle_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_emgsensor
    ADD CONSTRAINT feed_emgsensor_muscle_id_fkey FOREIGN KEY (muscle_id) REFERENCES feed_muscle(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_emgsensor_sensor_ptr_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_emgsensor
    ADD CONSTRAINT feed_emgsensor_sensor_ptr_id_fkey FOREIGN KEY (sensor_ptr_id) REFERENCES feed_sensor(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_emgsensor_side_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_emgsensor
    ADD CONSTRAINT feed_emgsensor_side_id_fkey FOREIGN KEY (side_id) REFERENCES feed_side(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_emgsetup_setup_ptr_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_emgsetup
    ADD CONSTRAINT feed_emgsetup_setup_ptr_id_fkey FOREIGN KEY (setup_ptr_id) REFERENCES feed_setup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_emgunit_created_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_emgunit
    ADD CONSTRAINT feed_emgunit_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_experiment_created_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_experiment
    ADD CONSTRAINT feed_experiment_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_experiment_study_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_experiment
    ADD CONSTRAINT feed_experiment_study_id_fkey FOREIGN KEY (study_id) REFERENCES feed_study(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_experiment_subj_devstage_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_experiment
    ADD CONSTRAINT feed_experiment_subj_devstage_id_fkey FOREIGN KEY (subj_devstage_id) REFERENCES feed_developmentstage(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_experiment_subject_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_experiment
    ADD CONSTRAINT feed_experiment_subject_id_fkey FOREIGN KEY (subject_id) REFERENCES feed_subject(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_illustration_created_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_illustration
    ADD CONSTRAINT feed_illustration_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_illustration_experiment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_illustration
    ADD CONSTRAINT feed_illustration_experiment_id_fkey FOREIGN KEY (experiment_id) REFERENCES feed_experiment(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_illustration_setup_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_illustration
    ADD CONSTRAINT feed_illustration_setup_id_fkey FOREIGN KEY (setup_id) REFERENCES feed_setup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_illustration_subject_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_illustration
    ADD CONSTRAINT feed_illustration_subject_id_fkey FOREIGN KEY (subject_id) REFERENCES feed_subject(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_muscle_created_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_muscle
    ADD CONSTRAINT feed_muscle_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_restraint_created_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_restraint
    ADD CONSTRAINT feed_restraint_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_sensor_created_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_sensor
    ADD CONSTRAINT feed_sensor_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_sensor_setup_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_sensor
    ADD CONSTRAINT feed_sensor_setup_id_fkey FOREIGN KEY (setup_id) REFERENCES feed_setup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_session_created_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_session
    ADD CONSTRAINT feed_session_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_session_experiment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_session
    ADD CONSTRAINT feed_session_experiment_id_fkey FOREIGN KEY (experiment_id) REFERENCES feed_experiment(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_session_subj_restraint_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_session
    ADD CONSTRAINT feed_session_subj_restraint_id_fkey FOREIGN KEY (subj_restraint_id) REFERENCES feed_restraint(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_setup_created_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_setup
    ADD CONSTRAINT feed_setup_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_setup_experiment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_setup
    ADD CONSTRAINT feed_setup_experiment_id_fkey FOREIGN KEY (experiment_id) REFERENCES feed_experiment(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_setup_technique_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_setup
    ADD CONSTRAINT feed_setup_technique_id_fkey FOREIGN KEY (technique_id) REFERENCES feed_technique(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_side_created_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_side
    ADD CONSTRAINT feed_side_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_sonochannel_channel_ptr_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_sonochannel
    ADD CONSTRAINT feed_sonochannel_channel_ptr_id_fkey FOREIGN KEY (channel_ptr_id) REFERENCES feed_channel(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_sonochannel_crystal1_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_sonochannel
    ADD CONSTRAINT feed_sonochannel_crystal1_id_fkey FOREIGN KEY (crystal1_id) REFERENCES feed_sonosensor(sensor_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_sonochannel_crystal2_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_sonochannel
    ADD CONSTRAINT feed_sonochannel_crystal2_id_fkey FOREIGN KEY (crystal2_id) REFERENCES feed_sonosensor(sensor_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_sonochannel_sono_unit_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_sonochannel
    ADD CONSTRAINT feed_sonochannel_sono_unit_id_fkey FOREIGN KEY (sono_unit_id) REFERENCES feed_sonounit(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_sonosensor_axisap_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_sonosensor
    ADD CONSTRAINT feed_sonosensor_axisap_id_fkey FOREIGN KEY (axisap_id) REFERENCES feed_anteriorposterioraxis(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_sonosensor_axisdepth_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_sonosensor
    ADD CONSTRAINT feed_sonosensor_axisdepth_id_fkey FOREIGN KEY (axisdepth_id) REFERENCES feed_depthaxis(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_sonosensor_axisdv_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_sonosensor
    ADD CONSTRAINT feed_sonosensor_axisdv_id_fkey FOREIGN KEY (axisdv_id) REFERENCES feed_dorsalventralaxis(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_sonosensor_muscle_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_sonosensor
    ADD CONSTRAINT feed_sonosensor_muscle_id_fkey FOREIGN KEY (muscle_id) REFERENCES feed_muscle(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_sonosensor_sensor_ptr_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_sonosensor
    ADD CONSTRAINT feed_sonosensor_sensor_ptr_id_fkey FOREIGN KEY (sensor_ptr_id) REFERENCES feed_sensor(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_sonosensor_side_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_sonosensor
    ADD CONSTRAINT feed_sonosensor_side_id_fkey FOREIGN KEY (side_id) REFERENCES feed_side(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_sonosetup_setup_ptr_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_sonosetup
    ADD CONSTRAINT feed_sonosetup_setup_ptr_id_fkey FOREIGN KEY (setup_ptr_id) REFERENCES feed_setup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_sonounit_created_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_sonounit
    ADD CONSTRAINT feed_sonounit_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_study_created_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_study
    ADD CONSTRAINT feed_study_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_studyprivate_created_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_studyprivate
    ADD CONSTRAINT feed_studyprivate_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_studyprivate_study_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_studyprivate
    ADD CONSTRAINT feed_studyprivate_study_id_fkey FOREIGN KEY (study_id) REFERENCES feed_study(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_subject_created_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_subject
    ADD CONSTRAINT feed_subject_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_subject_study_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_subject
    ADD CONSTRAINT feed_subject_study_id_fkey FOREIGN KEY (study_id) REFERENCES feed_study(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_subject_taxon_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_subject
    ADD CONSTRAINT feed_subject_taxon_id_fkey FOREIGN KEY (taxon_id) REFERENCES feed_taxon(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_taxon_created_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_taxon
    ADD CONSTRAINT feed_taxon_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_technique_created_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_technique
    ADD CONSTRAINT feed_technique_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_trial_behavior_primary_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_trial
    ADD CONSTRAINT feed_trial_behavior_primary_id_fkey FOREIGN KEY (behavior_primary_id) REFERENCES feed_behavior(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_trial_created_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_trial
    ADD CONSTRAINT feed_trial_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feed_trial_session_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_trial
    ADD CONSTRAINT feed_trial_session_id_fkey FOREIGN KEY (session_id) REFERENCES feed_session(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sensor_id_refs_sensor_ptr_id_36c09083; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY feed_emgelectrode
    ADD CONSTRAINT sensor_id_refs_sensor_ptr_id_36c09083 FOREIGN KEY (sensor_id) REFERENCES feed_emgsensor(sensor_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

